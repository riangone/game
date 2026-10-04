#!/usr/bin/env python3
"""Generate clause-level (sub-sentence) MP3 audio and timing metadata for 《小马过河》 preview.

Splits long sentences by punctuation (，, 。, ！, ？, ；, ：) to make shadowing / repetition
much easier for students, and provides precise durations for audio progress bar scrub/seek.
"""
import asyncio
import json
from pathlib import Path
import subprocess
import edge_tts

ROOT = Path(__file__).resolve().parent
OUT_DIR = ROOT / "audio" / "xiaoma_clause"
OUT_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR = ROOT / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-12%"

CLAUSES_DATA = [
    # Sentence 1: 小马要过河，看见一头老牛在喝水。
    {
        "sentId": "st1",
        "sentZh": "小马要过河，看见一头老牛在喝水。",
        "clauses": [
            {"id": "st1_c1", "zh": "小马要过河，", "py": "Xiǎomǎ yào guòhé,", "en": "The pony wanted to cross the river,", "jp": "子馬は川を渡ろうとして、"},
            {"id": "st1_c2", "zh": "看见一头老牛在喝水。", "py": "kànjiàn yìtóu lǎoniú zài hēshuǐ.", "en": "and saw an old ox drinking water.", "jp": "水を飲んでいる年老いた牛を見ました。"}
        ]
    },
    # Sentence 2: 小马问：“牛伯伯，我要过河，水深吗？”
    {
        "sentId": "st2",
        "sentZh": "小马问：“牛伯伯，我要过河，水深吗？”",
        "clauses": [
            {"id": "st2_c1", "zh": "小马问：", "py": "Xiǎomǎ wèn:", "en": "The pony asked,", "jp": "子馬は尋ねました。"},
            {"id": "st2_c2", "zh": "“牛伯伯，", "py": "“Niú bóbo,", "en": "“Uncle Ox,", "jp": "「牛のおじさん、"},
            {"id": "st2_c3", "zh": "我要过河，", "py": "wǒ yào guòhé,", "en": "I want to cross the river.", "jp": "川を渡りたいのですが、"},
            {"id": "st2_c4", "zh": "水深吗？”", "py": "shuǐ shēn ma?”", "en": "Is the water deep?”", "jp": "水は深いですか？」"}
        ]
    },
    # Sentence 3: 老牛说：“水很浅，你过得去。”
    {
        "sentId": "st3",
        "sentZh": "老牛说：“水很浅，你过得去。”",
        "clauses": [
            {"id": "st3_c1", "zh": "老牛说：", "py": "Lǎoniú shuō:", "en": "The old ox said,", "jp": "年老いた牛は言いました。"},
            {"id": "st3_c2", "zh": "“水很浅，", "py": "“Shuǐ hěn qiǎn,", "en": "“The water is shallow,", "jp": "「水はとても浅いよ、"},
            {"id": "st3_c3", "zh": "你过得去。”", "py": "nǐ guò de qù.”", "en": "you can cross it.”", "jp": "渡れるよ。」"}
        ]
    },
    # Sentence 4: 小马听了老牛的话，正要过河，突然，一只小松鼠从树上跳下来，大声说：“小马，别过河！水深得很呢！你会淹死的！”
    {
        "sentId": "st4",
        "sentZh": "小马听了老牛的话，正要过河，突然，一只小松鼠从树上跳下来，大声说：“小马，别过河！水深得很呢！你会淹死的！”",
        "clauses": [
            {"id": "st4_c1", "zh": "小马听了老牛的话，", "py": "Xiǎomǎ tīng le lǎoniú de huà,", "en": "The pony listened to the old ox,", "jp": "子馬は年老いた牛の話を聞いて、"},
            {"id": "st4_c2", "zh": "正要过河，", "py": "zhèng yào guòhé,", "en": "and was about to cross,", "jp": "まさに川を渡ろうとしたとき、"},
            {"id": "st4_c3", "zh": "突然，", "py": "tūrán,", "en": "suddenly,", "jp": "突然、"},
            {"id": "st4_c4", "zh": "一只小松鼠从树上跳下来，", "py": "yìzhī xiǎo sōngshǔ cóng shù shang tiào xiàlái,", "en": "a little squirrel jumped down from a tree,", "jp": "一匹の小さなリスが木から飛び降りてきて、"},
            {"id": "st4_c5", "zh": "大声说：", "py": "dàshēng shuō:", "en": "and shouted:", "jp": "大声で言いました。"},
            {"id": "st4_c6", "zh": "“小马，别过河！", "py": "“Xiǎomǎ, bié guòhé!", "en": "“Pony, don't cross!", "jp": "「子馬さん、川を渡らないで！"},
            {"id": "st4_c7", "zh": "水深得很呢！", "py": "shuǐ shēn de hěn ne!", "en": "The water is very deep!", "jp": "水はとても深いよ！"},
            {"id": "st4_c8", "zh": "你会淹死的！”", "py": "nǐ huì yānsǐ de!”", "en": "You'll drown!”", "jp": "溺れ死んじゃうよ！」"}
        ]
    },
    # Sentence 5: 听了小松鼠的话，小马不知道该怎么办，只好回家问妈妈。
    {
        "sentId": "st5",
        "sentZh": "听了小松鼠的话，小马不知道该怎么办，只好回家问妈妈。",
        "clauses": [
            {"id": "st5_c1", "zh": "听了小松鼠的话，", "py": "Tīng le xiǎo sōngshǔ de huà,", "en": "Hearing what the squirrel said,", "jp": "小さなリスの話を聞いて、"},
            {"id": "st5_c2", "zh": "小马不知道该怎么办，", "py": "xiǎomǎ bù zhīdào gāi zěnme bàn,", "en": "the pony didn't know what to do,", "jp": "子馬はどうすればいいか分からず、"},
            {"id": "st5_c3", "zh": "只好回家问妈妈。", "py": "zhǐhǎo huí jiā wèn māma.", "en": "so he had to go home and ask his mother.", "jp": "仕方なく家に帰ってお母さんに聞きました。"}
        ]
    },
    # Sentence 6: 妈妈说：“孩子，老牛又高又大，他会觉得水很浅；松鼠那么小，他一定会说水很深。河水是深还是浅，最好你自己去试试。”
    {
        "sentId": "st6",
        "sentZh": "妈妈说：“孩子，老牛又高又大，他会觉得水很浅；松鼠那么小，他一定会说水很深。河水是深还是浅，最好你自己去试试。”",
        "clauses": [
            {"id": "st6_c1", "zh": "妈妈说：", "py": "Māma shuō:", "en": "Mother said,", "jp": "お母さんは言いました。"},
            {"id": "st6_c2", "zh": "“孩子，", "py": "“Háizi,", "en": "“My child,", "jp": "「坊や、"},
            {"id": "st6_c3", "zh": "老牛又高又大，", "py": "lǎoniú yòu gāo yòu dà,", "en": "the ox is tall and big,", "jp": "牛は背が高くて大きいから、"},
            {"id": "st6_c4", "zh": "他会觉得水很浅；", "py": "tā huì juéde shuǐ hěn qiǎn;", "en": "so he feels the water is shallow;", "jp": "水を浅いと感じるのよ。"},
            {"id": "st6_c5", "zh": "松鼠那么小，", "py": "sōngshǔ nàme xiǎo,", "en": "the squirrel is so small,", "jp": "リスはあんなに小さいから、"},
            {"id": "st6_c6", "zh": "他一定会说水很深。", "py": "tā yídìng huì shuō shuǐ hěn shēn.", "en": "he is sure to say the water is deep.", "jp": "きっと水は深いと言うでしょう。"},
            {"id": "st6_c7", "zh": "河水是深还是浅，", "py": "Héshuǐ shì shēn háishi qiǎn,", "en": "Whether the river is deep or shallow,", "jp": "川の水が深いか浅いか、"},
            {"id": "st6_c8", "zh": "最好你自己去试试。”", "py": "zuìhǎo nǐ zìjǐ qù shìshi.”", "en": "you'd best go try it yourself.”", "jp": "自分で試してみるのが一番よ。」"}
        ]
    },
    # Sentence 7: 小马听了妈妈的话，又跑到河边，小心地过了河。
    {
        "sentId": "st7",
        "sentZh": "小马听了妈妈的话，又跑到河边，小心地过了河。",
        "clauses": [
            {"id": "st7_c1", "zh": "小马听了妈妈的话，", "py": "Xiǎomǎ tīng le māma de huà,", "en": "The pony listened to his mother,", "jp": "子馬はお母さんの話を聞いて、"},
            {"id": "st7_c2", "zh": "又跑到河边，", "py": "yòu pǎo dào hébiān,", "en": "ran back to the riverbank,", "jp": "また川辺に走って行き、"},
            {"id": "st7_c3", "zh": "小心地过了河。", "py": "xiǎoxīn de guò le hé.", "en": "and carefully crossed the river.", "jp": "注意深く川を渡りました。"}
        ]
    },
    # Sentence 8: 原来，河水既不像老牛说的那样浅，也不像松鼠说的那样深。
    {
        "sentId": "st8",
        "sentZh": "原来，河水既不像老牛说的那样浅，也不像松鼠说的那样深。",
        "clauses": [
            {"id": "st8_c1", "zh": "原来，", "py": "Yuánlái,", "en": "It turned out that,", "jp": "なんと、"},
            {"id": "st8_c2", "zh": "河水既不像老牛说的那样浅，", "py": "héshuǐ jì bú xiàng lǎoniú shuō de nàyàng qiǎn,", "en": "the river was neither as shallow as the ox had said,", "jp": "川の水は牛が言ったほど浅くもなく、"},
            {"id": "st8_c3", "zh": "也不像松鼠说的那样深。", "py": "yě bú xiàng sōngshǔ shuō de nàyàng shēn.", "en": "nor as deep as the squirrel had said.", "jp": "リスが言ったほど深くもありませんでした。"}
        ]
    }
]

def get_duration(file_path):
    try:
        res = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(file_path)],
            capture_output=True, text=True, check=True
        )
        return round(float(res.stdout.strip()), 3)
    except Exception as e:
        print(f"Error reading duration for {file_path}: {e}")
        return 2.0

async def main():
    print(f"Generating clause audio for {len(CLAUSES_DATA)} sentences...")
    sem = asyncio.Semaphore(4)

    tasks = []
    for s_idx, sent in enumerate(CLAUSES_DATA):
        for c_idx, clause in enumerate(sent["clauses"]):
            cid = clause["id"]
            target = OUT_DIR / f"{cid}.mp3"
            text = clause["zh"]

            async def gen(t_path=target, t_text=text, cid_name=cid):
                if t_path.exists() and t_path.stat().st_size > 1000:
                    return
                async with sem:
                    try:
                        comm = edge_tts.Communicate(t_text, VOICE, rate=RATE)
                        await comm.save(str(t_path))
                        print(f"Generated {cid_name}: {t_text}")
                    except Exception as err:
                        print(f"Failed {cid_name}: {err}")

            tasks.append(gen())

    await asyncio.gather(*tasks)
    print("Audio files generated. Measuring durations and computing timeline offsets...")

    # Calculate timings per sentence and global article timeline
    global_time = 0.0
    processed_data = []

    for s_idx, sent in enumerate(CLAUSES_DATA):
        sent_duration = 0.0
        processed_clauses = []
        sent_start_global = global_time

        for c_idx, clause in enumerate(sent["clauses"]):
            cid = clause["id"]
            target = OUT_DIR / f"{cid}.mp3"
            dur = get_duration(target)

            clause_entry = {
                "id": cid,
                "sentIndex": s_idx,
                "clauseIndex": c_idx,
                "zh": clause["zh"],
                "py": clause["py"],
                "en": clause["en"],
                "jp": clause["jp"],
                "audioUrl": f"audio/xiaoma_clause/{cid}.mp3",
                "duration": dur,
                "sentOffsetStart": round(sent_duration, 3),
                "sentOffsetEnd": round(sent_duration + dur, 3),
                "globalOffsetStart": round(global_time, 3),
                "globalOffsetEnd": round(global_time + dur, 3),
            }
            sent_duration += dur
            global_time += dur
            processed_clauses.append(clause_entry)

        processed_data.append({
            "sentId": sent["sentId"],
            "sentIndex": s_idx,
            "sentZh": sent["sentZh"],
            "duration": round(sent_duration, 3),
            "globalOffsetStart": round(sent_start_global, 3),
            "globalOffsetEnd": round(global_time, 3),
            "clauseCount": len(processed_clauses),
            "clauses": processed_clauses
        })

    meta_file = DATA_DIR / "xiaoma_clauses.json"
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump({
            "lesson": "xiaoma-guohe",
            "title": "小马过河",
            "totalSentences": len(processed_data),
            "totalClauses": sum(len(s["clauses"]) for s in processed_data),
            "totalDuration": round(global_time, 3),
            "sentences": processed_data
        }, f, ensure_ascii=False, indent=2)

    print(f"Saved metadata to {meta_file}. Total duration: {round(global_time, 2)}s across {sum(len(s['clauses']) for s in processed_data)} clauses.")

if __name__ == "__main__":
    asyncio.run(main())
