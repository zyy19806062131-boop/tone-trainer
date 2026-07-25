# 《新HSK教程1》(外研社, 2025年12月, HSK3.0) 课文原文 —— 逐句转录
# 来源: /Volumes/My PSSD/课件和教材/1.HSK/1.新HSK/新HSK 1/新hsk1教材.pdf (扫描版,逐页看图转录)
# 每课: id, 标题(教材真实课名), en标题, scenes[ {name, track, sents:[(zh, py_textbook, en)] } ]
# track = 官方配套音频轨号(教材课文栏印的 🔊 编号),音频在 新HSK 1/2026版新HSK1听力/<track>.mp3
# 规律: 每课三篇课文,音轨 N-1/N-3/N-5 为课文,双数轨为生词
# py_textbook = 教材印的带调拼音;"AI小语"的 AI 不入拼音流(拼音只写汉字部分),spokenZh 保留 AI
# 页码对照: 印刷页 = PDF页index - 13

LESSONS = [
  # L1 (印刷页001-003, PDF 14-16)
  {"id":"lesson-01","title":"AI小语，你好！","en":"Hello, AI Xiaoyu!","scenes":[
    {"name":"课文1 办公室打招呼","track":"1-1","sents":[
      # 用户定夺(07-21):不要"AI小语"称呼语,只留"你好";音频用指定区间截该轨内的"你好"
      ("你好！","Nǐ hǎo","Hello!",{"clip":(2.03,2.68)}),
      # 原句"王老师，你好！"——去人名策略(用户07-21):呼语去掉后与上句重复,由去重自动丢弃
      ("你好！","Nǐ hǎo","Hello!"),
    ]},
    {"name":"课文2 课堂问好","track":"1-3","sents":[
      ("大家好！","Dàjiā hǎo","Hello, everyone!"),
      ("老师，您好！","Lǎoshī nín hǎo","Hello, teacher!"),
      ("你们好！","Nǐmen hǎo","Hello, all!"),
      # 原句"你好，小语！"——同上,去呼语后重复自动丢弃
      ("你好！","Nǐ hǎo","Hello!"),
    ]},
    {"name":"课文3 致谢与告别","track":"1-5","sents":[
      ("谢谢！","Xièxie","Thank you!"),
      ("不客气！","Bú kèqi","You're welcome!"),
      ("同学们，再见！","Tóngxuémen zàijiàn","Goodbye, class!"),
      ("老师，再见！","Lǎoshī zàijiàn","Goodbye, teacher!"),
    ]},
  ]},
  # L2 (印刷页005-008, PDF 18-21)
  {"id":"lesson-02","title":"我叫李文","en":"My name is Li Wen","scenes":[
    {"name":"课文1 教室里认识学生","track":"2-1","sents":[
      ("请问，你叫什么名字？","Qǐngwèn nǐ jiào shénme míngzi","May I ask, what's your name?"),
      ("我叫陈天中。","Wǒ jiào Chén Tiānzhōng","My name is Chen Tianzhong."),
    ]},
    {"name":"课文2 校园里认错人","track":"2-3","sents":[
      # 原句"你好，安妮！"——去人名呼语后与L1"你好！"重复,由去重自动丢弃
      ("你好！","Nǐ hǎo","Hello!"),
      ("你好，陈天中！我不是安妮，我是白家月。","Nǐ hǎo Chén Tiānzhōng Wǒ bú shì Ānnī wǒ shì Bái Jiāyuè","Hello, Chen Tianzhong! I'm not Annie—I'm Bai Jiayue."),
      ("对不起！","Duìbuqǐ","Sorry!"),
      ("没关系！","Méi guānxi","It's okay!"),
    ]},
    {"name":"课文3 校园初次相遇","track":"2-5","sents":[
      ("你好！我叫李文。","Nǐ hǎo Wǒ jiào Lǐ Wén","Hello! My name is Li Wen."),
      ("你好！我叫白家月。","Nǐ hǎo Wǒ jiào Bái Jiāyuè","Hello! My name is Bai Jiayue."),
      ("很高兴认识你。","Hěn gāoxìng rènshi nǐ","Nice to meet you."),
      ("认识你我也很高兴。","Rènshi nǐ wǒ yě hěn gāoxìng","Nice to meet you too."),
    ]},
  ]},
  # L3 (印刷页010-014, PDF 23-27)
  {"id":"lesson-03","title":"我是中国人","en":"I'm Chinese","scenes":[
    {"name":"课文1 校园聊天","track":"3-1","sents":[
      ("我是中国人。","Wǒ shì Zhōngguó rén","I'm Chinese."),
      ("我是法国人。我的中文老师也是中国人。","Wǒ shì Fǎguó rén Wǒ de Zhōngwén lǎoshī yě shì Zhōngguó rén","I'm French. My Chinese language teacher is also Chinese."),
    ]},
    {"name":"课文2 看手机照片","track":"3-3","sents":[
      ("这是谁？","Zhè shì shéi","Who is this?"),
      ("这是我女朋友。","Zhè shì wǒ nǚpéngyou","This is my girlfriend."),
      ("你女朋友是哪国人？","Nǐ nǚpéngyou shì nǎ guó rén","What nationality is your girlfriend?"),
      ("她也是泰国人。","Tā yě shì Tàiguó rén","She is also Thai."),
    ]},
    {"name":"课文3 视频电话","track":"3-5","sents":[
      # 原句"喂，一飞！"——去人名呼语,音频取段内首个子段(喂)
      ("喂！","Wèi","Hi!",{"sub":"head"}),
      ("姐姐！","Jiějie","Sister!"),
      ("你工作还忙吗？","Nǐ gōngzuò hái máng ma","Are you still busy with work?"),
      ("对，还很忙。你也很忙吗？","Duì hái hěn máng Nǐ yě hěn máng ma","Yes, I'm still very busy. Are you busy too?"),
      ("我不太忙。我们很想你。","Wǒ bú tài máng Wǒmen hěn xiǎng nǐ","I'm not too busy. We miss you a lot."),
      ("我也想你们。","Wǒ yě xiǎng nǐmen","I miss you all too."),
    ]},
  ]},
  # L4 (印刷页018-024, PDF 31-37)
  {"id":"lesson-04","title":"我有两个孩子","en":"I have two children","scenes":[
    {"name":"课文1 家里聊天","track":"4-1","sents":[
      # "一飞忙吗？"人名是主语无法去除,保留(教材原句)
      ("一飞忙吗？","Yīfēi máng ma","Is Yifei busy?"),
      ("她很忙。","Tā hěn máng","She is very busy."),
      ("她有多少个学生？","Tā yǒu duōshao gè xuéshēng","How many students does she have?"),
      ("她有二十个学生。","Tā yǒu èrshí gè xuéshēng","She has twenty students."),
    ]},
    {"name":"课文2 公司休息聊天","track":"4-3","sents":[
      ("我有两个哥哥，你呢？","Wǒ yǒu liǎng gè gēge nǐ ne","I have two elder brothers. How about you?"),
      ("我没有哥哥。","Wǒ méiyǒu gēge","I don't have any elder brothers."),
      ("你家有几口人？","Nǐ jiā yǒu jǐ kǒu rén","How many people are there in your family?"),
      ("我家有四口人，爸爸、妈妈、妹妹和我。","Wǒ jiā yǒu sì kǒu rén bàba māma mèimei hé wǒ","There are four people in my family: my dad, my mom, my younger sister, and me."),
    ]},
    {"name":"课文3 街上偶遇","track":"4-5","sents":[
      ("这是您儿子吗？","Zhè shì nín érzi ma","Is this your son?"),
      ("是的。我有两个孩子，一个儿子，一个女儿。","Shì de Wǒ yǒu liǎng gè háizi yí gè érzi yí gè nǚér","Yes. I have two children, a son and a daughter."),
      ("您儿子几岁？","Nín érzi jǐ suì","How old is your son?"),
      ("他今年五岁。","Tā jīnnián wǔ suì","He is five years old."),
      ("您女儿多大？","Nín nǚér duō dà","How old is your daughter?"),
      ("她今年十二。","Tā jīnnián shíèr","She is twelve."),
    ]},
  ]},
  # L5 (印刷页027-032, PDF 40-45)
  {"id":"lesson-05","title":"今天我休息","en":"I'm off today","scenes":[
    {"name":"课文1 看日历","track":"5-1","sents":[
      ("今天几号？","Jīntiān jǐ hào","What's the date today?"),
      # 教材印"今天9月8号",数字按口语读法写汉字以逐字对齐
      ("今天九月八号。","Jīntiān jiǔ yuè bā hào","It's September 8."),
      ("星期几？","Xīngqī jǐ","What day is it today?"),
      ("星期日。今天我休息。","Xīngqīrì Jīntiān wǒ xiūxi","It's Sunday. I'm off today."),
    ]},
    {"name":"课文2 会做饭吗","track":"5-3","sents":[
      ("你会做饭吗？","Nǐ huì zuò fàn ma","Do you know how to cook?"),
      ("我会做。","Wǒ huì zuò","Yes, I do."),
      ("你会做什么？","Nǐ huì zuò shénme","What dishes can you make?"),
      ("我会做面条儿、饺子，也会做一些菜。星期天我也做饭。","Wǒ huì zuò miàntiáor jiǎozi yě huì zuò yìxiē cài Xīngqītiān wǒ yě zuò fàn","I can make noodles, jiaozi, and some other dishes. I also cook on Sundays."),
    ]},
    {"name":"课文3 下班聊新电脑","track":"5-5","sents":[
      # 原句"同乐，下班吗？"——去人名呼语,音频取段内尾部子段
      ("下班吗？","Xiàbān ma","Are you off work?",{"sub":"tail"}),
      ("下班。","Xiàbān","Yes, I am."),
      ("这是你的新电脑吗？","Zhè shì nǐ de xīn diànnǎo ma","Is this your new computer?"),
      ("是的，是我的新电脑。","Shì de shì wǒ de xīn diànnǎo","Yes, it's my new computer."),
      ("真好看！","Zhēn hǎokàn","It looks really nice!"),
      ("我也很喜欢它。","Wǒ yě hěn xǐhuan tā","I really like it too."),
    ]},
  ]},
  # L6 (印刷页035-039, PDF 48-52)
  {"id":"lesson-06","title":"你的手机号是多少？","en":"What's your cell phone number?","scenes":[
    {"name":"课文1 要手机号","track":"6-1","sents":[
      # 原句"家月，你的手机号是多少？"——去人名呼语,音频取尾部
      ("你的手机号是多少？","Nǐ de shǒujīhào shì duōshao","What's your cell phone number?",{"sub":"tail"}),
      # 号码显示阿拉伯数字(用户07-22定);声调格只挂汉字,数字段音频照读(逐位、1读幺)
      ("我的手机号是+33 601493190。","Wǒ de shǒujīhào shì","My cell phone number is +33 601493190."),
      ("我的手机号是+86 13552721160。","Wǒ de shǒujīhào shì","My cell phone number is +86 13552721160."),
      ("好的。","Hǎo de","Alright."),
    ]},
    {"name":"课文2 明天去超市","track":"6-3","sents":[
      # 原句"家月，明天你去哪儿？"——去人名呼语,音频取尾部
      ("明天你去哪儿？","Míngtiān nǐ qù nǎr","Where are you going tomorrow?",{"sub":"tail"}),
      ("我想去超市买东西。","Wǒ xiǎng qù chāoshì mǎi dōngxi","I want to go to the supermarket to buy groceries."),
      ("你去超市买什么？","Nǐ qù chāoshì mǎi shénme","What are you going to buy at the supermarket?"),
      ("我想买些牛奶。","Wǒ xiǎng mǎi xiē niúnǎi","I want to buy some milk."),
    ]},
    {"name":"课文3 周末晚餐安排","track":"6-5","sents":[
      ("星期天我们去哪儿吃晚饭？","Xīngqītiān wǒmen qù nǎr chī wǎnfàn","Where are we going for dinner on Sunday?"),
      ("我还想去西安饭店。","Wǒ hái xiǎng qù Xīān Fàndiàn","I'd like to go to Xi'an Restaurant again."),
      ("那边的包子非常好吃，我想吃包子。","Nàbiān de bāozi fēicháng hǎochī wǒ xiǎng chī bāozi","The steamed stuffed buns there are very delicious—I'd love to eat some."),
      ("妈妈，我想吃米饭，不想吃包子。","Māma wǒ xiǎng chī mǐfàn bù xiǎng chī bāozi","Mom, I'd rather have rice—not steamed stuffed buns."),
      ("好的。我们怎么去？","Hǎo de Wǒmen zěnme qù","Alright. How shall we get there?"),
      ("坐出租车去。","Zuò chūzūchē qù","Let's take a taxi."),
    ]},
  ]},
  # L7 (印刷页045-051, PDF 58-64)
  {"id":"lesson-07","title":"我晚上六点半下班","en":"I'll finish work at 6:30 in the evening","scenes":[
    {"name":"课文1 电话约时间","track":"7-1","sents":[
      ("现在几点？","Xiànzài jǐ diǎn","What time is it now?"),
      ("早上八点四十。","Zǎoshang bā diǎn sìshí","It's 8:40 in the morning."),
      ("我上午十点十分有课。","Wǒ shàngwǔ shí diǎn shí fēn yǒu kè","I have a class at 10:10 in the morning."),
      ("好的，我们下午两点见吧。","Hǎo de wǒmen xiàwǔ liǎng diǎn jiàn ba","Alright, let's meet at 2:00 in the afternoon."),
    ]},
    {"name":"课文2 约看电影","track":"7-3","sents":[
      ("下午我想去电影院看电影，你去吗？","Xiàwǔ wǒ xiǎng qù diànyǐngyuàn kàn diànyǐng nǐ qù ma","I want to go to the cinema to watch a movie this afternoon. Are you going?"),
      ("我不想去，下午还有事。","Wǒ bù xiǎng qù xiàwǔ hái yǒu shì","I don't want to go. I still have something to do this afternoon."),
      ("好的。明天呢？","Hǎo de Míngtiān ne","Okay. How about tomorrow?"),
      ("我明天下午两点还上课呢，四点半下课。","Wǒ míngtiān xiàwǔ liǎng diǎn hái shàngkè ne sì diǎn bàn xiàkè","I have a class tomorrow afternoon at 2:00 and it finishes at 4:30."),
    ]},
    {"name":"课文3 下班安排","track":"7-5","sents":[
      ("喂，你在哪儿呢？","Wèi nǐ zài nǎr ne","Hey, where are you?"),
      ("我在家里呢。","Wǒ zài jiā li ne","I'm at home."),
      ("我晚上六点半下班。","Wǒ wǎnshang liù diǎn bàn xiàbān","I'll finish work at 6:30 in the evening."),
      ("我八点去医院上班。","Wǒ bā diǎn qù yīyuàn shàngbān","I'll go to work at the hospital at 8:00."),
      ("好的，你去店里买些菜吧。","Hǎo de nǐ qù diàn li mǎi xiē cài ba","Alright, could you go to the store to buy some vegetables?"),
      ("好，我十分钟后去。","Hǎo wǒ shí fēnzhōng hòu qù","Okay, I'll go in ten minutes."),
    ]},
  ]},
  # L8 (印刷页054-059, PDF 67-72)
  {"id":"lesson-08","title":"我爸爸也在医院工作","en":"My father also works at a hospital","scenes":[
    {"name":"课文1 找小猫","track":"8-1","sents":[
      ("房间外有一只小猫。","Fángjiān wài yǒu yì zhī xiǎo māo","There is a little cat outside the room."),
      ("我没看见，它在哪儿呢？","Wǒ méi kànjiàn tā zài nǎr ne","I don't see it. Where is it?"),
      ("它在桌子下呢。","Tā zài zhuōzi xià ne","It's under the table."),
      ("这只小猫真漂亮！","Zhè zhī xiǎo māo zhēn piàoliang","This little cat is so beautiful!"),
    ]},
    {"name":"课文2 约见面地点","track":"8-3","sents":[
      ("我们在哪儿见呢？","Wǒmen zài nǎr jiàn ne","Where shall we meet?"),
      ("在学校书店前见吧。","Zài xuéxiào shūdiàn qián jiàn ba","Let's meet in front of the school bookstore."),
      ("好的。下午两点你能到吗？","Hǎo de Xiàwǔ liǎng diǎn nǐ néng dào ma","Okay. Can you arrive at 2:00 in the afternoon?"),
      ("我能到。我在学校吃午饭。","Wǒ néng dào Wǒ zài xuéxiào chī wǔfàn","Yes, I can. I'll have lunch at school."),
    ]},
    {"name":"课文3 医院聊工作","track":"8-5","sents":[
      # 原句"小胡，还没吃饭呢？"——去人名呼语(小+姓),音频取尾部
      ("还没吃饭呢？","Hái méi chī fàn ne","Haven't you eaten yet?",{"sub":"tail"}),
      ("没吃呢。","Méi chī ne","No, I haven't."),
      ("大医院病人多，医生非常忙。","Dà yīyuàn bìngrén duō yīshēng fēicháng máng","There are a lot of patients in big hospitals, and doctors are very busy."),
      ("是的。我爸爸也在医院工作，他也非常忙。","Shì de Wǒ bàba yě zài yīyuàn gōngzuò tā yě fēicháng máng","True. My father also works at a hospital, and he's extremely busy too."),
      ("你家有两个医生？","Nǐ jiā yǒu liǎng gè yīshēng","So there are two doctors in your family?"),
      ("对。","Duì","Yes."),
    ]},
  ]},
  # L9 (印刷页061-066, PDF 74-79)
  {"id":"lesson-09","title":"我明天上午在学校学习","en":"I'll be studying at school tomorrow morning","scenes":[
    {"name":"课文1 约看电影","track":"9-1","sents":[
      ("学校前边有一家电影院。","Xuéxiào qiánbian yǒu yì jiā diànyǐngyuàn","There is a cinema in front of the school."),
      ("对。我们晚上去那个电影院看电影吧。","Duì Wǒmen wǎnshang qù nàge diànyǐngyuàn kàn diànyǐng ba","Yes. Let's go to the cinema to watch a movie tonight."),
      ("好！我们七点在电影院外边见，好吗？","Hǎo Wǒmen qī diǎn zài diànyǐngyuàn wàibian jiàn hǎo ma","Great! Let's meet outside the cinema at 7:00, okay?"),
      ("好的，晚上七点见！","Hǎo de wǎnshang qī diǎn jiàn","Okay, see you at 7:00 in the evening!"),
    ]},
    {"name":"课文2 椅子上的书","track":"9-3","sents":[
      ("椅子上有一本中文书，那是谁的书？","Yǐzi shang yǒu yì běn Zhōngwén shū nà shì shéi de shū","There is a Chinese book on the chair. Whose book is that?"),
      ("是我的书，谢谢。这是我的第二本中文书。","Shì wǒ de shū xièxie Zhè shì wǒ de dìèr běn Zhōngwén shū","It's my book, thanks. This is my second Chinese book."),
      ("不客气。你明天上午在哪儿？","Bú kèqi Nǐ míngtiān shàngwǔ zài nǎr","You're welcome. Where will you be tomorrow morning?"),
      ("我明天上午在学校学习。","Wǒ míngtiān shàngwǔ zài xuéxiào xuéxí","I'll be studying at school tomorrow morning."),
    ]},
    {"name":"课文3 周六做什么","track":"9-5","sents":[
      ("明天星期六，你做什么？","Míngtiān Xīngqīliù nǐ zuò shénme","Tomorrow is Saturday. What are you going to do?"),
      ("我白天在家里读书，晚上和朋友们去外边唱歌。","Wǒ báitiān zài jiā li dúshū wǎnshang hé péngyoumen qù wàibian chàng gē","I will read at home during the day and go out to sing with my friends in the evening."),
      ("你唱歌很好听。","Nǐ chàng gē hěn hǎotīng","You sing very well."),
      ("谢谢！您星期六做什么？","Xièxie Nín Xīngqīliù zuò shénme","Thank you! What will you do on Saturday?"),
      ("我在家里做饭、看电视，和孩子们、小狗玩。","Wǒ zài jiā li zuò fàn kàn diànshì hé háizimen xiǎo gǒu wán","I will cook, watch TV, and play with my children and my little dog at home."),
      ("我也有一只小狗。","Wǒ yě yǒu yì zhī xiǎo gǒu","I also have a little dog."),
    ]},
  ]},
  # L10 (印刷页070-075, PDF 83-88)
  {"id":"lesson-10","title":"这儿的苹果真便宜！","en":"The apples here are really affordable!","scenes":[
    {"name":"课文1 买杯子","track":"10-1","sents":[
      ("请问，有杯子吗？","Qǐngwèn yǒu bēizi ma","Excuse me, do you have any cups?"),
      ("有，杯子在这边。","Yǒu bēizi zài zhèbiān","Yes, the cups are over here."),
      ("多少钱一个？","Duōshao qián yí gè","How much is one?"),
      ("这些五块钱一个，那些十块钱一个。","Zhèxiē wǔ kuài qián yí gè nàxiē shí kuài qián yí gè","These are five yuan each, and those are ten yuan each."),
      ("我买这个吧。","Wǒ mǎi zhège ba","I'll take this one, please."),
    ]},
    {"name":"课文2 买苹果","track":"10-3","sents":[
      ("这儿的水果真不少！","Zhèr de shuǐguǒ zhēn bù shǎo","There's so much fruit here!"),
      ("您想买什么？","Nín xiǎng mǎi shénme","What would you like to buy?"),
      ("我想买两斤苹果。","Wǒ xiǎng mǎi liǎng jīn píngguǒ","I'd like two jin of apples, please."),
      ("苹果三块五一斤。这些七块二，七块钱吧。","Píngguǒ sān kuài wǔ yì jīn Zhèxiē qī kuài èr qī kuài qián ba","The apples are 3.5 yuan per jin. That's 7.2 yuan in total—let's round it down to 7 yuan."),
      ("好的，这儿的苹果真便宜！","Hǎo de zhèr de píngguǒ zhēn piányi","Great! The apples here are really affordable!"),
    ]},
    {"name":"课文3 买衣服","track":"10-5","sents":[
      ("这家商店衣服真多！这件一百元，怎么样？","Zhè jiā shāngdiàn yīfu zhēn duō Zhè jiàn yìbǎi yuán zěnmeyàng","There are so many clothes in this store! This one is 100 yuan. What do you think?"),
      ("好看，也不贵。","Hǎokàn yě bú guì","It looks great, and it's not expensive."),
      # 小雪/小明是句子主语,无法去名,保留教材原句
      ("小雪能穿，买一件吧。","Xiǎoxuě néng chuān mǎi yí jiàn ba","Xiaoxue can wear it. Let's get one."),
      ("好的。小明能穿吗？","Hǎo de Xiǎomíng néng chuān ma","Okay. Do you think Xiaoming can wear it too?"),
      ("不能。这些是女孩子穿的衣服，男孩子的衣服在那儿。","Bù néng Zhèxiē shì nǚ háizi chuān de yīfu nán háizi de yīfu zài nàr","No. These are girls' clothes. The boys' section is over there."),
      ("好的。","Hǎo de","Alright."),
    ]},
  ]},
  # L11 (印刷页078-083, PDF 91-96)
  {"id":"lesson-11","title":"我读大学呢","en":"I'm studying at university","scenes":[
    {"name":"课文1 路上找饭店","track":"11-1","sents":[
      # 原句"喂，李文，你什么时候能到饭店？"——呼语夹在句中,连"喂"一起去掉,音频取尾部
      ("你什么时候能到饭店？","Nǐ shénme shíhou néng dào fàndiàn","When will you arrive at the restaurant?",{"sub":"tail"}),
      ("还不知道，正在找呢。它是不是在超市后边？","Hái bù zhīdào zhèngzài zhǎo ne Tā shì bu shì zài chāoshì hòubian","Not sure yet. I'm looking for it now. Is it behind the supermarket?"),
      ("是的。你开车没开车？","Shì de Nǐ kāichē méi kāichē","Yes, it is. Are you driving or not?"),
      ("我没开车，坐车呢。","Wǒ méi kāichē zuò chē ne","No, I'm not driving. I'm taking a taxi."),
    ]},
    {"name":"课文2 还在读大学吗","track":"11-3","sents":[
      ("你还在读大学吗？","Nǐ hái zài dú dàxué ma","Are you still studying at university?"),
      ("对，我读大学呢，还是大学生。","Duì wǒ dú dàxué ne hái shì dàxuéshēng","Yes. I'm studying at university, and I'm still an undergraduate."),
      ("你们学习忙不忙？","Nǐmen xuéxí máng bu máng","Are you busy with your studies?"),
      ("非常忙，我学医，我们的课很多。","Fēicháng máng wǒ xué yī wǒmen de kè hěn duō","Very busy. I major in medicine, and we have a lot of classes."),
    ]},
    {"name":"课文3 弟弟起床了吗","track":"11-5","sents":[
      ("弟弟起床没起床呢？","Dìdi qǐchuáng méi qǐchuáng ne","Has the younger brother gotten up yet?"),
      ("没起床呢，还在睡觉。","Méi qǐchuáng ne hái zài shuìjiào","Not yet. He's still sleeping."),
      ("还睡呢？他今天去不去那里？","Hái shuì ne Tā jīntiān qù bu qù nàlǐ","Still sleeping? Is he going there today?"),
      ("去哪里？","Qù nǎlǐ","Going where?"),
      ("去超市。","Qù chāoshì","To the supermarket."),
      ("我昨天问他，他对我说，他不去，他今天要和小朋友玩。","Wǒ zuótiān wèn tā tā duì wǒ shuō tā bú qù tā jīntiān yào hé xiǎopéngyǒu wán","I asked him yesterday. He told me he's not going—he wants to play with his friends today."),
    ]},
  ]},
  # L12 (印刷页086-091, PDF 99-104)
  {"id":"lesson-12","title":"昨天下雪了","en":"It snowed yesterday","scenes":[
    {"name":"课文1 电话问天气","track":"12-1","sents":[
      ("今天天气怎么样？","Jīntiān tiānqì zěnmeyàng","How's the weather today?"),
      ("这里的天不太好，下雨了。","Zhèlǐ de tiān bú tài hǎo xià yǔ le","It's not great here. It's raining."),
      ("雨大吗？","Yǔ dà ma","Is it raining heavily?"),
      ("有点儿大，我觉得很冷。","Yǒudiǎnr dà wǒ juéde hěn lěng","A bit, and I feel really cold."),
    ]},
    {"name":"课文2 电梯里聊下雪","track":"12-3","sents":[
      ("昨天下雪了。","Zuótiān xià xuě le","It snowed yesterday."),
      ("是的，太冷了。","Shì de tài lěng le","Yes, it's too cold."),
      ("你昨天没来公司，生病了？","Nǐ zuótiān méi lái gōngsī shēngbìng le","You didn't come to the company yesterday. Were you sick?"),
      ("对，我昨天去医院看病了。","Duì wǒ zuótiān qù yīyuàn kànbìng le","Yes, I went to the hospital to see a doctor yesterday."),
    ]},
    {"name":"课文3 看医生","track":"12-5","sents":[
      ("医生，我病了。","Yīshēng wǒ bìng le","Doctor, I'm not feeling well."),
      ("我看看。你觉得怎么样？","Wǒ kànkan Nǐ juéde zěnmeyàng","Let me take a look. How are you feeling?"),
      ("我很冷。","Wǒ hěn lěng","I feel very cold."),
      ("好的，吃一点儿药，今天休息半天吧。","Hǎo de chī yìdiǎnr yào jīntiān xiūxi bàn tiān ba","Alright. Take some medicine and rest for half a day today."),
      # "好的。"与L6重复,去重自动丢弃
      ("好的。","Hǎo de","OK."),
      ("回家后再喝些热水。","Huí jiā hòu zài hē xiē rè shuǐ","Make sure to drink some warm water after you get home."),
    ]},
  ]},
  # L13 (印刷页095-100, PDF 108-113)
  {"id":"lesson-13","title":"请给我一杯茶","en":"A cup of tea, please","scenes":[
    {"name":"课文1 问老师问题","track":"13-1","sents":[
      # 原句"王老师，我可以再问您一个问题吗？"——去人名呼语,音频取尾部
      ("我可以再问您一个问题吗？","Wǒ kěyǐ zài wèn nín yí gè wèntí ma","May I ask you one more question?",{"sub":"tail"}),
      ("可以。你有什么问题？","Kěyǐ Nǐ yǒu shénme wèntí","Yes, of course. What's your question?"),
      ("那个小店卖不卖手机？","Nàge xiǎo diàn mài bu mài shǒujī","Does that small shop sell cell phones?"),
      ("我不知道。你可以打电话问一下。","Wǒ bù zhīdào Nǐ kěyǐ dǎ diànhuà wèn yíxià","I'm not sure. You can call to ask."),
    ]},
    {"name":"课文2 咖啡馆点早餐","track":"13-3","sents":[
      ("女士，请坐！您喝什么？","Nǚshì qǐng zuò Nín hē shénme","Madam, have a seat, please! What would you like to drink?"),
      ("我看一下。请给我一杯牛奶。","Wǒ kàn yíxià Qǐng gěi wǒ yì bēi niúnǎi","Let me have a look. I'll have a glass of milk, please."),
      ("好的。您还要什么？","Hǎo de Nín hái yào shénme","Alright. Would you like anything else?"),
      ("我还没吃早饭，再要这个面包和鸡蛋吧。","Wǒ hái méi chī zǎofàn zài yào zhège miànbāo hé jīdàn ba","I haven't had breakfast yet, so I'll have a fried egg on bread."),
    ]},
    {"name":"课文3 点饺子","track":"13-5","sents":[
      ("先生，请坐！您要什么？","Xiānsheng qǐng zuò Nín yào shénme","Sir, have a seat, please! What would you like to order?"),
      ("我要一斤饺子。","Wǒ yào yì jīn jiǎozi","I'd like one jin of jiaozi."),
      # 教材印"一斤饺子40个",数字写汉字对齐
      ("好的。一斤饺子四十个。","Hǎo de Yì jīn jiǎozi sìshí gè","Alright. One jin of jiaozi has forty pieces."),
      ("四十个太多了，我要一半吧。","Sìshí gè tài duō le wǒ yào yíbàn ba","Forty is too many. I'll have half of that."),
      ("半斤二十个。您想喝什么？","Bàn jīn èrshí gè Nín xiǎng hē shénme","Half is twenty. What would you like to drink?"),
      ("请给我一杯茶吧。","Qǐng gěi wǒ yì bēi chá ba","I'll have a cup of tea, please."),
    ]},
  ]},
  # L14 (印刷页103-109, PDF 116-122)
  {"id":"lesson-14","title":"我看了一个电影","en":"I watched a movie","scenes":[
    {"name":"课文1 聊课外旅行","track":"14-1","sents":[
      # "王老师"在宾语位置无法去除,保留教材原句
      ("你们上火车后看见王老师了吗？","Nǐmen shàng huǒchē hòu kànjiàn Wáng lǎoshī le ma","Did you see Ms. Wang after boarding the train?"),
      ("没看见。中午车开后，有些人在看书，有些人睡觉了。","Méi kànjiàn Zhōngwǔ chē kāi hòu yǒuxiē rén zài kàn shū yǒuxiē rén shuìjiào le","No, we didn't. After the train departed at noon, some people were reading, while others fell asleep."),
      ("你呢？","Nǐ ne","What about you?"),
      ("我看了一个电影。","Wǒ kànle yí gè diànyǐng","I watched a movie."),
    ]},
    {"name":"课文2 课堂问学习情况","track":"14-3","sents":[
      ("你们会说汉语了，也会写汉字了吗？","Nǐmen huì shuō Hànyǔ le yě huì xiě Hànzì le ma","You can speak Chinese now. Can you also write Chinese characters?"),
      ("我们都会写了。","Wǒmen dōu huì xiě le","We can all write them now."),
      ("老师，我听不见。","Lǎoshī wǒ tīng bú jiàn","Teacher, I can't hear you."),
      ("请大家不要说话！请听老师的问题：你们都会写哪些汉字了？","Qǐng dàjiā búyào shuōhuà Qǐng tīng lǎoshī de wèntí Nǐmen dōu huì xiě nǎxiē Hànzì le","Everyone, please stop talking! Listen to my question: Which Chinese characters can you write?"),
      ("我会写这些字了，您看！","Wǒ huì xiě zhèxiē zì le nín kàn","I can write these characters. Look!"),
    ]},
    {"name":"课文3 孩子上学了","track":"14-5","sents":[
      ("明年女儿上中学。","Míngnián nǚér shàng zhōngxué","Our daughter will start middle school next year."),
      ("对。儿子也上小学了。","Duì Érzi yě shàng xiǎoxué le","That's right. Our son will also start primary school."),
      ("我们家有了一个中学生。","Wǒmen jiā yǒule yí gè zhōngxuéshēng","We will have a middle school student in our family."),
      ("还有了一个小学生。","Hái yǒule yí gè xiǎoxuéshēng","And a primary school student."),
      ("上学后，他们都忙了。","Shàngxué hòu tāmen dōu máng le","Once they start school, they will both be busy."),
      ("是的。太晚了，睡觉吧。","Shì de Tài wǎn le shuìjiào ba","Yes. It's too late. Let's go to bed."),
    ]},
  ]},
  # L15 (印刷页112-117, PDF 125-130)
  {"id":"lesson-15","title":"大兴机场见！","en":"See you at Daxing Airport!","scenes":[
    {"name":"课文1 品尝中餐","track":"15-1","sents":[
      ("你们爱吃哪个菜？","Nǐmen ài chī nǎge cài","Which dish do you like?"),
      ("我喜欢这个，也喜欢那个。","Wǒ xǐhuan zhège yě xǐhuan nàge","I like this one, and that one too."),
      ("这些菜都好吃，还很好看。","Zhèxiē cài dōu hǎochī hái hěn hǎokàn","These dishes are all delicious, and they look great too."),
      ("我爱吃中国菜，也喜欢做。大家多吃点儿。","Wǒ ài chī Zhōngguó cài yě xǐhuan zuò Dàjiā duō chī diǎnr","I love eating Chinese food, and I also enjoy cooking it. Everyone, eat more!"),
    ]},
    {"name":"课文2 想去哪儿旅行","track":"15-3","sents":[
      ("你们都想去哪儿？","Nǐmen dōu xiǎng qù nǎr","Where do you all want to go?"),
      ("去年我和男朋友去了西安，今年我想去北京。","Qùnián wǒ hé nánpéngyou qùle Xīān jīnnián wǒ xiǎng qù Běijīng","My boyfriend and I went to Xi'an last year, and I want to visit Beijing this year."),
      ("前几年我去了西安，非常好玩儿。今年我也想去北京。","Qián jǐ nián wǒ qùle Xīān fēicháng hǎowánr Jīnnián wǒ yě xiǎng qù Běijīng","I went to Xi'an a few years ago, and it was really fun. This year, I want to go to Beijing too."),
      # "王老师"在句中无法去除,保留教材原句
      ("我和王老师都是北京人，北京非常漂亮。","Wǒ hé Wáng lǎoshī dōu shì Běijīng rén Běijīng fēicháng piàoliang","Ms. Wang and I are both from Beijing. Beijing is very beautiful."),
    ]},
    {"name":"课文3 约机场见","track":"15-5","sents":[
      ("你们的飞机到北京要几个小时？","Nǐmen de fēijī dào Běijīng yào jǐ gè xiǎoshí","How many hours will your flight take to get to Beijing?"),
      ("九个小时。","Jiǔ gè xiǎoshí","Nine hours."),
      ("我家人都在北京，星期天我姐姐也有时间，她可以去机场接你们，你们也可以住我家。","Wǒ jiārén dōu zài Běijīng Xīngqītiān wǒ jiějie yě yǒu shíjiān tā kěyǐ qù jīchǎng jiē nǐmen nǐmen yě kěyǐ zhù wǒ jiā","My whole family lives in Beijing. My sister will be free on Sunday. She can pick you up at the airport, and you can stay at my home."),
      ("我们星期日早上八点到大兴机场，早不早？","Wǒmen Xīngqīrì zǎoshang bā diǎn dào Dàxīng Jīchǎng zǎo bu zǎo","We'll arrive at Daxing Airport at 8:00 on Sunday morning. Is that early?"),
      ("不早。","Bù zǎo","Not early at all."),
      ("谢谢老师！那我们和您姐姐在大兴机场见！","Xièxie lǎoshī Nà wǒmen hé nín jiějie zài Dàxīng Jīchǎng jiàn","Thank you, teacher! Then we'll meet your sister at Daxing Airport!"),
    ]},
  ]},
]
