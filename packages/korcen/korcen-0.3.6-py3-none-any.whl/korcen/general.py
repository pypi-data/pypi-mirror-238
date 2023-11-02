import re
from better_profanity import profanity
from collections import OrderedDict


def general(text:str):
    text = re.sub('𝗌', 's', text)
    text = re.sub('𝘴', 's', text)
    text = re.sub('𝙨', 's', text)
    text = re.sub('𝚜', 's', text)
    text = re.sub('𝐬', 's', text)
    text = re.sub('𝑠', 's', text)
    text = re.sub('𝒔', 's', text)
    text = re.sub('𝓈', 's', text)
    text = re.sub('𝓼', 's', text)
    text = re.sub('𝔰', 's', text)
    text = re.sub('𝖘', 's', text)
    text = re.sub('𝕤', 's', text)
    text = re.sub('ｓ', 's', text)
    text = re.sub('ⓢ', 's', text)
    text = re.sub('⒮', 's', text)
    text = re.sub('🅢', 's', text)
    text = re.sub('🆂', 's', text)
    text = re.sub('🅂', 's', text)
    text = re.sub('𝖾', 'e', text)
    text = re.sub('𝘦', 'e', text)
    text = re.sub('𝙚', 'e', text)
    text = re.sub('𝚎', 'e', text)
    text = re.sub('𝐞', 'e', text)
    text = re.sub('𝑒', 'e', text)
    text = re.sub('𝒆', 'e', text)
    text = re.sub('ℯ', 'e', text)
    text = re.sub('𝓮', 'e', text)
    text = re.sub('𝔢', 'e', text)
    text = re.sub('𝖊', 'e', text)
    text = re.sub('𝕖', 'e', text)
    text = re.sub('ｅ', 'e', text)
    text = re.sub('ⓔ', 'e', text)
    text = re.sub('⒠', 'e', text)
    text = re.sub('🅔', 'e', text)
    text = re.sub('🅴', 'e', text)
    text = re.sub('🄴', 'e', text)
    text = re.sub('є', 'e', text)
    text = re.sub('𝗑', 'x', text)
    text = re.sub('𝘹', 'x', text)
    text = re.sub('𝙭', 'x', text)
    text = re.sub('𝚡', 'x', text)
    text = re.sub('𝐱', 'x', text)
    text = re.sub('𝑥', 'x', text)
    text = re.sub('𝒙', 'x', text)
    text = re.sub('𝓍', 'x', text)
    text = re.sub('𝔁', 'x', text)
    text = re.sub('𝔵', 'x', text)
    text = re.sub('𝖝', 'x', text)
    text = re.sub('𝕩', 'x', text)
    text = re.sub('ｘ', 'x', text)
    text = re.sub('ⓧ', 'x', text)
    text = re.sub('⒳', 'x', text)
    text = re.sub('🅧', 'x', text)
    text = re.sub('🆇', 'x', text)
    text = re.sub('🅇', 'x', text)
    text = re.sub('₨', 'rs', text)
    text = re.sub('ų', 'u', text)
    text = re.sub('ç', 'c', text)
    text = re.sub('Ｆ', 'F', text)
    text = re.sub('Ｋ', 'K', text)
    text = re.sub('Ｃ', 'C', text)
    text = re.sub('Ｕ', 'U', text)
    newtext = text.lower()

    text = re.sub('ㅗ먹어', 'ㅗ', newtext)
    text = re.sub('오ㅗㅗ', '', text)
    text = re.sub('오ㅗ', '', text)
    text = re.sub('해ㅗㅗ', '', text)
    text = re.sub('해ㅗ', '', text)
    text = re.sub('호ㅗㅗ', '', text)
    text = re.sub('호ㅗ', '', text)
    text = re.sub('로ㅗㅗ', '', text)
    text = re.sub('로ㅗ', '', text)
    text = re.sub('옹ㅗㅗ', '', text)
    text = re.sub('옹ㅗ', '', text)
    text = re.sub('롤ㅗㅗ', '', text)
    text = re.sub('롤ㅗ', '', text)
    text = re.sub('요ㅗ', '', text)
    text = re.sub('우ㅗ', '', text)
    text = re.sub('하ㅗ', '', text)
    text = re.sub('ㅗㅗ오', '', text)
    text = re.sub('ㅗ오', '', text)
    text = re.sub('ㅗㅗ호', '', text)
    text = re.sub('ㅗ호', '', text)
    text = re.sub('ㅗㅗ로', '', text)
    text = re.sub('ㅗ로', '', text)
    text = re.sub('ㅗㅗ옹', '', text)
    text = re.sub('ㅗ옹', '', text)
    text = re.sub('ㅗㅗ롤', '', text)
    text = re.sub('ㅗ롤', '', text)
    text = re.sub('ㅗ요', '', text)
    text = re.sub('ㅗ우', '', text)
    text = re.sub('ㅗ하', '', text)
    text = re.sub('오ㅗㅗㅗㅗ', '', text)
    text = re.sub('오ㅗㅗㅗ', '', text)
    text = re.sub('호ㅗㅗㅗㅗ', '', text)
    text = re.sub('호ㅗㅗㅗ', '', text)
    text = re.sub('로ㅗㅗㅗㅗ', '', text)
    text = re.sub('로ㅗㅗㅗ', '', text)
    text = re.sub('옹ㅗㅗㅗㅗ', '', text)
    text = re.sub('옹ㅗㅗㅗ', '', text)
    text = re.sub('롤ㅗㅗㅗㅗ', '', text)
    text = re.sub('롤ㅗㅗㅗ', '', text)
    text = re.sub('요ㅗㅗㅗ', '', text)
    text = re.sub('우ㅗㅗㅗ', '', text)
    text = re.sub('하ㅗㅗㅗ', '', text)
    text = re.sub('ㅇㅗ', '', text)
    text = re.sub('ㅗㄷ', '', text)
    text = re.sub('ㅗㅜ', '', text)
    text = re.sub('rㅗ', '', text)
    text = re.sub('ㅗr', '', text)
    text = re.sub('sㅗ', '', text)
    text = re.sub('ㅗs', '', text)
    text = re.sub('eㅗ', '', text)
    text = re.sub('ㅗe', '', text)
    text = re.sub('fㅗ', '', text)
    text = re.sub('ㅗf', '', text)
    text = re.sub('aㅗ', '', text)
    text = re.sub('ㅗa', '', text)
    text = re.sub('qㅗ', '', text)
    text = re.sub('ㅗq', '', text)
    text = re.sub('ㅗw', '', text)
    text = re.sub('wㅗ', '', text)
    text = re.sub('ㅗd', '', text)
    text = re.sub('dㅗ', '', text)
    text = re.sub('ㅗg', '', text)
    text = re.sub('gㅗ', '', text)
    text = re.sub(' ', '', text)
    fuckyou = ["ㅗ", "┻", "┴", "┹", "_ㅣ_",
                "_/_", "⊥", "_ |\_", "_|\_", "_ㅣ\_", "_I_", "丄"]
    for i in fuckyou:
        if i in text:
            return True

    fuck = ["tq", "qt"]
    for i in fuck:
        if i == newtext:
            return True
    text = re.sub('118', '', newtext)
    text = re.sub('218', '', text)
    text = re.sub('318', '', text)
    text = re.sub('418', '', text)
    text = re.sub('518', '', text)
    text = re.sub('618', '', text)
    text = re.sub('718', '', text)
    text = re.sub('818', '', text)
    text = re.sub('918', '', text)
    text = re.sub('018', '', text)
    text = re.sub('련', '놈', newtext)
    text = re.sub('뇬', '놈', text)
    text = re.sub('놈', '놈', text)
    text = re.sub('넘', '놈', text)
    text = re.sub('8분', '', text)
    text = re.sub(' ', '', text)
    fuck = ["씨8", "18아", "18놈", "tㅂ", "t발", "ㅆㅍ",
            "sibal", "sival", "sibar", "sibak", "sipal", "siqk", "tlbal", "tlval", "tlbar", "tlbak", "tlpal", "tlqk",
            "시bal", "시val", "시bar", "시bak", "시pal", "시qk", "시bal", "시val", "시bar", "시bak", "시pal", "시qk",
            "si바", "si발", "si불", "si빨", "si팔", "tl바", "tl발", "tl불", "tl빨", "tl팔",
            "siba", "tlba", "siva", "tlva", "tlqkf", "10발놈", "10발년", "tlqkd", "si8", "10R놈", "시8", "십8", "s1bal", "sib알"]
    for i in fuck:
        if i in text:
            return True
    text = re.sub(r'\^', 'ㅅ', newtext)
    text = re.sub('人', 'ㅅ', text)
    text = re.sub('∧', 'ㅅ', text)
    text = re.sub('／＼', 'ㅅ', text)
    text = re.sub('/＼', 'ㅅ', text)
    text = re.sub('㉦', 'ㅅ', text)
    text = re.sub('丨발', '시발', text)
    text = re.sub('丨벌', '시발', text)
    text = re.sub('丨바', '시발', text)
    text = re.sub('甘', 'ㅂ', text)
    text = re.sub('廿', 'ㅂ', text)
    text = re.sub('己', 'ㄹ', text)
    text = re.sub('卜', 'ㅏ', text)
    text = re.sub('l', 'ㅣ', text)
    text = re.sub('r', 'ㅏ', text)
    text = re.sub('ᐲ', 'ㅅ', text)
    text = re.sub('ᗨ', 'ㅂ', text)
    text = re.sub('시ㅣ', '시', text)
    text = re.sub('씨ㅣ', '씨', text)
    text = re.sub('ㅅ1', '시', text)
    text = re.sub('ㅍㅅㅍ', '', text)
    text = re.sub("[^ㄱ-힣]", "", text)
    fuck = ["시ㅂ", "시ㅏㄹ", "씨ㅂ", "씨ㅏㄹ", "ㅣ발", "ㅆ발", "ㅅ발", "ㅅㅂ", "ㅆㅂ", "ㅆ바", "ㅅ바",
            "시ㅂㅏ", "ㅅㅂㅏ", "시ㅏㄹ", "씨ㅏㄹ", "ㅅ불", "ㅆ불", "ㅅ쁠", "ㅆ뿔", "ㅆㅣ발", "ㅅㅟ발", "ㅅㅣㅂㅏ",
            "ㅣ바알", "ㅅ벌", "^^ㅣ벌", "ㅆ삐라", "씨ㅃ"]
    for i in fuck:
        if i in text:
            return True

    text = re.sub('다시 방', '', text)
    text = re.sub('다시 불러', '', text)
    text = re.sub('시발음', '', text)
    text = re.sub('시발택시', '', text)
    text = re.sub('시발자동차', '', text)
    text = re.sub('정치발', '', text)
    text = re.sub('시발점', '', text)
    text = re.sub('시발유', '', text)
    text = re.sub('시발역', '', text)
    text = re.sub('시발수뢰', '', text)
    text = re.sub('아저씨바', '', text)
    text = re.sub('아저씨발', '', text)
    text = re.sub('시바견', '', text)
    text = re.sub('벌어', '', text)
    text = re.sub('시바이누', '', text)
    text = re.sub('시바스리갈', '', text)
    text = re.sub('시바산', '', text)
    text = re.sub('시바신', '', text)
    text = re.sub('오리발', '', text)
    text = re.sub('발끝', '', text)
    text = re.sub('다시바', '', text)
    text = re.sub('다시팔', '', text)
    text = re.sub('비슈누시바', '', text)
    text = re.sub('시바핫카이', '', text)
    text = re.sub('시바타이쥬', '', text)
    text = re.sub('데스티니시바', '', text)
    text = re.sub('시바루', '', text)
    text = re.sub('시바료타로', '', text)
    text = re.sub('시바라스시', '', text)
    text = re.sub('임시방편', '', text)
    text = re.sub('젤리', '', text)
    text = re.sub('발사', '', text)
    text = re.sub('크시야', '', text)
    text = re.sub('크시', '', text)
    text = re.sub('어찌', '', text)
    text = re.sub('가시방석', '', text)
    text = re.sub('발로란트방', '', text)
    text = re.sub('발로란트', '', text)
    text = re.sub('씨발라', '', text)
    text = re.sub('무시발언', '', text)
    text = re.sub('일시불', '', text)
    text = re.sub('우리', '', text)
    text = re.sub('혹시', '', text)
    text = re.sub('아조씨', '', text)
    text = re.sub('아저씨', '', text)
    text = re.sub('바로', '', text)
    text = re.sub('저거시', '', text)
    text = re.sub('우리발', '', text)
    text = re.sub('피시방', '', text)
    text = re.sub('피씨방', '', text)
    text = re.sub('방장', '', text)
    text = re.sub('시바사키', '', text)
    text = re.sub('시발차', '', text)
    text = re.sub('로벅스', '', text)
    text = re.sub('쉬바나', '', text)
    text = re.sub('벌었는데', '', text)
    text = re.sub('엠씨방', '', text)
    text = re.sub('빨리', '', text)
    text = re.sub('파엠', '', text)
    text = re.sub('벌금', '', text)
    text = re.sub('시방향', '', text)
    text = re.sub('불법', '', text)
    text = re.sub('할시', '', text)
    text = re.sub('발릴', '', text)
    text = re.sub('발표', '', text)
    text = re.sub('방송', '', text)
    text = re.sub('역시', '', text)
    text = re.sub('바보', '', text)
    text = re.sub('쿨리발리', '', text)
    text = re.sub('아', '', text)
    text = re.sub('이', '', text)
    text = re.sub('일', '', text)
    text = re.sub('의', '', text)
    text = re.sub('하시바라 이노스케', '', text)
    text = re.sub("[^가-힣]", "", text)
    text = re.sub('련', '놈', text)
    text = re.sub('뇬', '놈', text)
    text = re.sub('놈', '놈', text)
    text = re.sub('넘', '놈', text)
    fuck = ["시발", "씨발", "시봘", "씨봘", "씨바", "시바", "샤발", "씌발", "씹발", "시벌", "시팔", "싯팔",
            "씨빨", "씨랼", "씨파", "띠발", "띡발", "띸발", "싸발", "십발", "슈발", "야발", "씨불", "씨랄",
            "쉬발", "쓰발", "쓔발", "쌰발", "쉬발", "쒸발", "씨팔", "씨밝", "씨밯", "쑤발", "치발", "샤발",
            "발씨", "리발", "씨볼", "찌발", "씨비바라랄", "시바랄", "씨바라", "쒸팔", "쉬팔", "씨밮", "쒸밮", "시밮",
            "씨삐라", "씨벌", "슈벌", "시불", "시부렝", "씨부렝", "시부랭", "씨부랭", "시부랭", "발놈시", "뛰발",
            "뛰봘", "뜨발", "뜨벌", "띄발", "씨바알", "샤빨", "샤발", "스벌", "쓰벌", "신발련", "신발년", "신발놈", "띠발",
            "띠바랄", "시방", "씨방", "씨부련", "시부련", "씨잇발", "씨잇파알", "씨잇바알", "시잇발", "시잇바알", "쒸이발",
            "쉬이빨", "씹팔", "쉬바", "시병발신", "씱빩", "쉬바난", "쉬바놈", "쉬바녀", "쉬바년", "쉬바노마,쉬바새", "쉬불", "쉬이바", "시벨놈", "시뱅놈", "시봉새"]
    for i in fuck:
        if i in text:
            return True

    text = re.sub('련', '놈', newtext)
    text = re.sub('뇬', '놈', text)
    text = re.sub('놈', '놈', text)
    text = re.sub('넘', '놈', text)
    fuck = ["18것", "18놈", "18럼", "18롬", "18새끼",
            "18세끼", "18세리", "18섹", "18쉑", "10쉑"]
    for i in fuck:
        if i in text:
            return True

    text = re.sub(' ', '', newtext)
    text = re.sub("opgg", "", text)
    text = re.sub("op.gg", "", text)
    bullshit1 = ["wlfkf", "g랄", "g럴", "g롤", "g뢀", "giral"]
    for i in bullshit1:
        if i in text:
            return True
    text = re.sub("g랄", "지랄", newtext)
    text = re.sub('己', 'ㄹ', text)
    text = re.sub("[^ㄱ-힣]", "", text)
    text = re.sub("있지", "", text)
    text = re.sub("없지", "", text)
    text = re.sub("하지", "", text)
    ext = re.sub('알았지', '', text)
    text = re.sub('몰랐지', '', text)
    text = re.sub('근데', '', text)
    text = re.sub('지근거', '', text)
    text = re.sub('지근하', '', text)
    text = re.sub('지근지근', '', text)
    text = re.sub('지근속근', '', text)
    text = re.sub('속든지근', '', text)
    text = re.sub("근", "ㄹ", text)
    text = re.sub("ㄹㅇ", "", text)
    bullshit1 = ["ㅈㄹ", "지ㄹ", "ㅈ랄", "ㅈ라"]
    for i in bullshit1:
        if i in text:
            return True

    text = re.sub("[^가-힣]", "", newtext)
    text = re.sub("있지", "", text)
    text = re.sub("없지", "", text)
    text = re.sub("하지", "", text)
    text = re.sub('지랄탄', '', text)
    text = re.sub('지랄버릇', '', text)
    text = re.sub('이', '', text)
    text = re.sub('알았지', '', text)
    text = re.sub('몰랐지', '', text)
    text = re.sub('근데', '', text)
    text = re.sub('미지근', '', text)
    bullshit2 = ["지랄", "찌랄", "지럴", "지롤", "랄지", "쥐랄", "쮜랄", "지뢀", "띄랄"]
    for i in bullshit2:
        if i in text:
            return True

    text = re.sub('0등신', '', newtext)
    text = re.sub('1등신', '', text)
    text = re.sub('2등신', '', text)
    text = re.sub('3등신', '', text)
    text = re.sub('4등신', '', text)
    text = re.sub('5등신', '', text)
    text = re.sub('6등신', '', text)
    text = re.sub('7등신', '', text)
    text = re.sub('8등신', '', text)
    text = re.sub('9등신', '', text)
    text = re.sub("[^ㄱ-힣]", "", text)
    text = re.sub('빙', '병', text)
    text = re.sub('븅', '병', text)
    text = re.sub('등', '병', text)
    text = re.sub('붱', '병', text)
    text = re.sub('뵝', '병', text)
    text = re.sub('뼝', '병', text)
    text = re.sub('싄', '신', text)
    text = re.sub('씬', '신', text)
    text = re.sub('우', '', text)
    text = re.sub('웅', '', text)
    asshole = ["ㅄ", "ㅂㅅ", "병ㅅ", "ㅂ신", "ㅕㅇ신", "ㅂㅇ신", "뷰신"]
    for i in asshole:
        if i in text:
            return True
    text = re.sub("[^가-힣]", "", text)
    text = re.sub('영', '', text)
    text = re.sub('엉', '', text)
    asshole = ["병신", "병딱", "벼신", "붱신", "뼝신", "뿽신", "삥신", "병시니", "병형신"]
    for i in asshole:
        if i in text:
            return True

    text = re.sub('전염병', '', newtext)
    text = re.sub('감염병', '', text)
    text = re.sub("[^가-힣]", "", text)
    motherfucker = ["염병", "엠병", "옘병", "염병", "얨병", "옘뼝"]
    for i in motherfucker:
        if i in text:
            return True

    text = re.sub("[^가-힣]", "", newtext)
    text = re.sub('왜꺼져', '', text)
    text = re.sub('꺼져요', '', text)
    text = re.sub('이꺼져', '', text)
    text = re.sub('꺼져서', '', text)
    text = re.sub('내꺼져', '', text)
    text = re.sub('제꺼져', '', text)
    text = re.sub('꺼져있', '', text)
    text = re.sub('꺼져도', '', text)
    text = re.sub('계속꺼져', '', text)
    text = re.sub('꺼져가', '', text)
    if "꺼져" in text:
        return True

    text = re.sub("[^가-힣]", "", newtext)
    shit = ["엿같", "엿가튼", "엿먹어", "뭣같은"]
    for i in shit:
        if i in text:
            return True

    sonofbitch = ["rotorl", "rotprl", "sib새", "AH끼", "sㅐ끼"]
    for i in sonofbitch:
        if i in text:
            return True

    text = re.sub(r'\^', 'ㅅ', newtext)
    text = re.sub('H', 'ㅐ', text)
    text = re.sub('새로', '', text)
    text = re.sub('77', 'ㄲ', text)
    text = re.sub('l', 'ㅣ', text)
    text = re.sub(' ', '', text)
    text = re.sub('10새', '새끼', text)
    text = re.sub('10섹', '새끼', text)
    text = re.sub('10쌔', '새끼', text)
    text = re.sub('10쎄', '새끼', text)
    text = re.sub('10새', '새끼', text)
    text = re.sub('10쉑', '새끼', text)
    text = re.sub('🐦', '새', text)
    text = re.sub("[^ㄱ-힣]", "", text)
    sonofbitch = ["ㅅㄲ", "ㅅ끼", "ㅆ끼", "색ㄲㅣ", "ㅆㅐㄲㅑ", "ㅆㅐㄲㅣ"]
    for i in sonofbitch:
        if i in text:
            return True

    text = re.sub("[^가-힣]", "", text)
    text = re.sub('의새끼', '', text)
    text = re.sub('애', '', text)
    text = re.sub('에', '', text)
    text = re.sub('루세끼', '', text)
    text = re.sub('시세끼', '', text)
    text = re.sub('세끼먹', '', text)
    text = re.sub('고양이새끼', '', text)
    text = re.sub('호랑이새끼', '', text)
    text = re.sub('말새끼', '', text)
    text = re.sub('사자새끼', '', text)
    text = re.sub('범새끼', '', text)
    text = re.sub('삵새끼', '', text)
    text = re.sub('키보드', '', text)
    text = re.sub('새끼손', '', text)
    sonofbitch = ["새끼", "쉐리", "쌔끼", "썌끼", "쎼끼", "쌬끼", "샠끼", "세끼", "샊", "쌖", "섺", "쎆", "십새", "새키", "씹색", "새까", "새꺄",
                    "새뀌", "새끠", "새캬", "색꺄", "색끼", "섹히", "셁기", "셁끼", "셐기", "셰끼", "셰리", "쉐꺄", "십색꺄", "십떼끼", "십데꺄", "십때끼", "십새꺄", "십새캬", "쉑히"]
    for i in sonofbitch:
        if i in text:
            return True

    dick = ["w같은"]
    for i in dick:
        if i in newtext:
            return True
    text = re.sub('丕', '조', newtext)
    text = re.sub('刀卜', '까', text)
    text = re.sub("[^ㄱ-힣]", "", text)
    text = re.sub('줫습니다', '', text)
    text = re.sub('쫒아', '', text)
    text = re.sub('쫒기다', '', text)
    text = re.sub('쫒기라', '', text)
    text = re.sub('쫒기로', '', text)
    text = re.sub('쫒기를', '', text)
    text = re.sub('쫒기며', '', text)
    text = re.sub('쫒기는', '', text)
    text = re.sub('쫒기나', '', text)
    text = re.sub('쫒겨', '', text)
    text = re.sub('쫒겻', '', text)
    text = re.sub('쫒겼', '', text)
    text = re.sub('쫒았', '', text)
    text = re.sub('쫒다', '', text)
    text = re.sub('줫는', '', text)
    text = re.sub('줫어', '', text)
    text = re.sub('줬는', '', text)
    text = re.sub('줫군', '', text)
    text = re.sub('줬다', '', text)
    text = re.sub('줬어', '', text)
    text = re.sub('천조', '', text)
    text = re.sub('쫒기', '', text)
    dick = ["ㅈ같", "ㅈ망", "ㅈ까", "ㅈ경", "ㅈ가튼"]
    for i in dick:
        if i in text:
            return True
    text = re.sub("[^가-힣]", "", text)
    text = re.sub('해줫더니', '', text)
    dick = ["좆", "촟", "조까", "좈", "쫒", "졷", "좃", "줮",
            "좋같", "좃같", "좃물", "좃밥", "줫", "좋밥", "좋물", "좇"]
    for i in dick:
        if i in text:
            return True

    damn = ["썅", "씨앙", "씨양", "샤앙", "쌰앙"]
    for i in damn:
        if i in text:
            return True

    swear = ["tq", "qt"]
    for i in swear:
        if text == i:
            return True

    whatthefuck = ["뻑유", "뻐킹", "뻐큐", "빡큐", "뿩큐", "뻑큐", "빡유", "뻒큐"]
    for i in whatthefuck:
        if i in text:
            return True

    shutup = ["닥쳐", "닭쳐", "닥치라", "아가리해"]
    for i in shutup:
        if i in text:
            return True

    text = re.sub(r'[0-9]+', '', newtext)
    sonofagun = ["dog새"]
    for i in sonofagun:
        if i in text:
            return True
    text = re.sub("[^ㄱ-힣]", "", newtext)
    sonofagun = ["개ㅐ색"]
    for i in sonofagun:
        if i in text:
            return True
    text = re.sub('0개', '', newtext)
    text = re.sub('1개', '', text)
    text = re.sub('2개', '', text)
    text = re.sub('3개', '', text)
    text = re.sub('4개', '', text)
    text = re.sub('5개', '', text)
    text = re.sub('6개', '', text)
    text = re.sub('7개', '', text)
    text = re.sub('8개', '', text)
    text = re.sub('9개', '', text)
    text = re.sub('0개', '', text)
    text = re.sub('1년', '', text)
    text = re.sub('2년', '', text)
    text = re.sub('3년', '', text)
    text = re.sub('4년', '', text)
    text = re.sub('5년', '', text)
    text = re.sub('6년', '', text)
    text = re.sub('7년', '', text)
    text = re.sub('8년', '', text)
    text = re.sub('9년', '', text)
    text = re.sub('🐕', '개', text)
    text = re.sub('🐦', '새', text)
    text = re.sub('재밌게 놈', '', text)
    text = re.sub("[^가-힣]", "", text)
    text = re.sub('있게', '', text)
    text = re.sub('년생', '', text)
    text = re.sub('무지개색', '', text)
    text = re.sub('떠돌이개', '', text)
    text = re.sub('에게', '', text)
    text = re.sub('넘는', '', text)
    text = re.sub('소개', '', text)
    text = re.sub('생긴게', '', text)
    sonofagun = ["개같", "개가튼", "개쉑", "개스키", "개세끼", "개색히", "개가뇬", "개새기", "개쌔기", "개쌔끼", "쌖", "쎆", "새긔", "개소리", "개년", "개소리",
                    "개드립", "개돼지", "개씹창", "개간나", "개스끼", "개섹기", "개자식", "개때꺄", "개때끼", "개발남아", "개샛끼", "개가든", "개가뜬", "개가턴", "개가툰", "개가튼",
                    "개갇은", "개갈보", "개걸레", "개너마", "개너므", "개넌", "개넘", "개녀나", "개년", "개노마", "개노무새끼", "개논", "개놈", "개뇨나", "개뇬", "개뇸", "개뇽", "개눔",
                    "개느마", "개늠", "개때꺄", "개때끼", "개떼끼", "개랙기", "개련", "개발남아", "개발뇬", "개색", "개색끼", "개샊", "개샛끼", "개샛키", "개샛킹", "개샛히", "개샜끼",
                    "개생키", "개샠", "개샤끼", "개샤킥", "개샥", "개샹늠", "개세끼", "개세리", "개세키", "개섹히", "개섺", "개셃", "개셋키", "개셐", "개셰리", "개솩", "개쇄끼", "개쇅",
                    "개쇅끼", "개쇅키", "개쇗", "개쇠리", "개쉐끼", "개쉐리", "개쉐키", "개쉑", "개쉑갸", "개쉑기", "개쉑꺄", "개쉑끼", "개쉑캬", "개쉑키", "개쉑히", "개쉢", "개쉨",
                    "개쉬끼", "개쉬리", "개쉽", "개스끼", "개스키", "개습", "개습세", "개습쌔", "개싀기", "개싀끼", "개싀밸", "개싀킈", "개싀키", "개싏", "개싑창", "개싘",
                    "개시끼", "개시퀴", "개시키", "개식기", "개식끼", "개식히", "개십새", "개십팔", "개싯기", "개싯끼", "개싯키", "개싴", "개쌍넘", "개쌍년", "개쌍놈", "개쌍눔",
                    "개쌍늠", "개쌍연", "개쌍영", "개쌔꺄", "개쌔끼", "개쌕", "개쌕끼", "개쌰깨", "개썅", "개쎄", "개쎅", "개쎼키", "개쐐리", "개쒜", "개쒝", "개쒯", "개쒸", "개쒸빨놈",
                    "개쒹기", "개쓉", "개쒹기", "개쓉", "개씀", "개씁", "개씌끼", "개씨끼", "개씨팕", "개씨팔", "개잡것", "개잡년", "개잡놈", "개잡뇬", "개젓", "개젖", "개젗", "개졋",
                    "개졎", "개조또", "개조옷", "개족", "개좃", "개좆", "개좇", "개지랄", "개지럴", "개창년", "개허러", "개허벌년", "개호러", "개호로", "개후랄", "개후레", "개후로",
                    "개후장", "걔섀끼", "걔잡넘", "걔잡년", "걔잡뇬", "게가튼", "게같은", "게너마", "게년", "게노마", "게놈", "게뇨나", "게뇬", "게뇸", "게뇽", "게눔", "게늠",
                    "게띠발넘", "게부랄", "게부알", "게새끼", "게새리", "게새키", "게색", "게색기", "게색끼", "게샛키", "게세꺄", "게자지", "게잡넘", "게잡년", "게잡뇬", "게젓",
                    "게좆", "계같은뇬", "계뇬", "계뇽", "쉬댕", "쉬뎅"]
    for i in sonofagun:
        if i in text:
            return True

    return False