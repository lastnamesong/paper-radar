#!/usr/bin/env python3
"""Send a run's top papers to Telegram.

Reads every `scouting/P*/<date>.md`, takes the 🥇🥈🥉 sections, ranks them by
score and sends the best N (default 3): title, authors, date, one-line summary,
why it matters, score and arXiv link.

    python3 scouting/notify-telegram.py [--date YYYY-MM-DD] [--top 3] [--dry-run]
    python3 scouting/notify-telegram.py --selftest

Needs TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in the environment (never in the repo).
"""
import argparse, glob, json, os, re, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDALS = ("🥇", "🥈", "🥉")


def parse_report(text):
    """Return one dict per medal section of a report."""
    papers = []
    for sec in re.split(r"(?m)^## ", text)[1:]:
        if not sec.startswith(MEDALS):
            continue
        title = re.search(r"(?m)^\*\*(.+)\*\*\s*$", sec)
        link = re.search(r"(?m)^\[arXiv:([\w.\-/]+)\]\([^)]*\)(.*)$", sec)
        score = re.search(r"\*\*점수 (\d+)/15\*\*", sec)
        if not (title and link and score):
            continue
        # fields after the link: authors · venue · source · code label
        fields = [f.strip() for f in link.group(2).split("·") if f.strip()]
        papers.append({
            "title": title.group(1),
            "id": link.group(1),
            "authors": fields[0] if fields else "",
            "score": int(score.group(1)),
            "summary": first_bullet(sec, "(b)"),
            "reason": first_bullet(sec, "(c)"),
        })
    return papers


def first_bullet(sec, tag):
    """First `- ` line under the `### (x)` subsection, bold markers stripped."""
    m = re.search(r"(?ms)^### \(%s\)[^\n]*\n(.*?)(?=^### |\Z)" % re.escape(tag[1]), sec)
    if m:
        b = re.search(r"(?m)^- (.+)$", m.group(1))
        if b:
            return b.group(1).replace("**", "").strip()
    return ""


def published_dates(ids):
    """arXiv id -> YYYY-MM-DD; empty dict if the API is unreachable."""
    url = "https://export.arxiv.org/api/query?max_results=%d&id_list=%s" % (len(ids), ",".join(ids))
    try:
        xml = urllib.request.urlopen(url, timeout=30).read().decode()
    except Exception:
        return {}
    out = {}
    for entry in xml.split("<entry>")[1:]:
        i = re.search(r"arxiv\.org/abs/([\w.\-/]+?)(?:v\d+)?</id>", entry)
        d = re.search(r"<published>(\d{4}-\d{2}-\d{2})", entry)
        if i and d:
            out[i.group(1)] = d.group(1)
    return out


def format_message(papers, date, dates):
    lines = ["📡 %s 논문 브리핑" % date]
    for n, p in enumerate(papers, 1):
        lines += ["", "%d. %s" % (n, p["title"]),
                  "%s · %s" % (p["authors"][:80], dates.get(p["id"], "날짜 미확인")),
                  "요약: %s" % p["summary"],
                  "관련: %s" % p["reason"],
                  "점수 %d/15 · https://arxiv.org/abs/%s" % (p["score"], p["id"])]
    return "\n".join(lines)[:4000]  # Telegram caps a message at 4096 chars


def collect(date):
    if not date:
        found = sorted(glob.glob(os.path.join(ROOT, "scouting", "P*", "????-??-??.md")))
        if not found:
            sys.exit("no scouting reports found")
        date = os.path.basename(found[-1])[:-3]
    papers = []
    for f in glob.glob(os.path.join(ROOT, "scouting", "P*", date + ".md")):
        papers += parse_report(open(f, encoding="utf-8").read())
    return date, sorted(papers, key=lambda p: -p["score"])


def selftest():
    sample = """# t

## 🥇 논문 1

**Soft Exo Control**
[arXiv:2611.00001](https://arxiv.org/abs/2611.00001) · A. Kim, B. Lee · arXiv preprint · source: keyword-sweep

**점수 11/15** · R3 · N2

### (b) 논문 요지
- 외골격 보조력 제어를 학습으로 대체
- **문제** — x

### (c) 시사점
- 보행 보조 제어에 바로 적용 가능

## 🥈 논문 2

**Tactile VTLA**
[arXiv:2611.00002](https://arxiv.org/abs/2611.00002) · C. Park · T-RO

**점수 13/15** · R3

### (b) 논문 요지
- 촉각을 VLA에 결합

### (c) 시사점
- 접촉 풍부 조작에 유리

## 📋 기준 통과

| x |
"""
    ps = parse_report(sample)
    assert [p["id"] for p in ps] == ["2611.00001", "2611.00002"], ps
    assert ps[0]["summary"] == "외골격 보조력 제어를 학습으로 대체" and ps[0]["authors"] == "A. Kim, B. Lee"
    msg = format_message(sorted(ps, key=lambda p: -p["score"]), "2026-11-08", {"2611.00002": "2026-11-07"})
    assert msg.index("Tactile VTLA") < msg.index("Soft Exo"), msg
    assert "날짜 미확인" in msg and "2026-11-07" in msg
    print("selftest ok")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date")
    ap.add_argument("--top", type=int, default=3)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    date, papers = collect(a.date)
    papers = papers[: a.top]
    if not papers:
        sys.exit("no medal sections in the %s reports" % date)
    msg = format_message(papers, date, published_dates([p["id"] for p in papers]))
    if a.dry_run:
        return print(msg)
    token, chat = os.environ["TELEGRAM_BOT_TOKEN"], os.environ["TELEGRAM_CHAT_ID"]
    data = urllib.parse.urlencode({"chat_id": chat, "text": msg,
                                   "disable_web_page_preview": "true"}).encode()
    r = json.load(urllib.request.urlopen("https://api.telegram.org/bot%s/sendMessage" % token, data, timeout=30))
    assert r.get("ok"), r


if __name__ == "__main__":
    main()
