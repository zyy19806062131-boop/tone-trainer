# 《新HSK教程2》(外研社, HSK3.0) 课文原文 —— 逐句转录
# 来源: /Volumes/My PSSD/教材库/01_成套教材/xin-hsk-jiaocheng/新HSK 2/New HSK Course 2 (HSK3.0).pdf
#       扫描版无文字层,逐页渲染成图看图转录(印刷页 = PDF页index - 14)
# 结构: 每课四篇课文——课文1/2/3 为人物对话(头像气泡)、课文4 为叙述体短文
# 音轨: 课文 N-1/N-3/N-5/N-7,双数轨为生词(不入本表);音频在 新HSK2+配套音频(1)/<track>.mp3
# 切分单位: 对话体「一个气泡＝一条」(与音频停顿对齐);叙述体逐句拆
# 拼音: 取教材印刷版(变调 bú/yí/yì、轻声无调号),不用 pypinyin 生成;
#       py 串统一过下方 _PUNC 清洗,只留字母+调号+空格(compile_lib 的输入契约)
LESSONS = [
{"id":"lesson-01","title":"她请我们吃了北京烤鸭","en":"She treated us to Peking Duck","scenes":[
  {"name":"课文1 机场接机","track":"1-1","sents":[
    ("请问，您是王一飞老师的姐姐吗？","Qǐngwèn nín shì Wáng Yīfēi lǎoshī de jiějie ma","May I ask, are you Teacher Wang Yifei's older sister?"),
    ("是的，你们就是她的学生吧？","Shì de nǐmen jiù shì tā de xuéshēng ba","Yes, and you two must be her students, right?"),
    ("对。我是白家月，她是安妮。","Duì Wǒ shì Bái Jiāyuè tā shì Ānnī","Exactly. I'm Bai Jiayue, and this is Annie."),
    ("你们好，我叫王一雪。一飞给我打电话了，让我来接你们。","Nǐmen hǎo wǒ jiào Wáng Yīxuě Yīfēi gěi wǒ dǎ diànhuà le ràng wǒ lái jiē nǐmen","Hello, I'm Wang Yixue. Yifei called me and asked me to pick you up."),
    ("谢谢您。","Xièxie nín","Thank you very much."),
    ("不客气。","Bú kèqi","You're welcome."),
  ]},
  {"name":"课文2 车里初次聊北京","track":"1-3","sents":[
    ("你们是第一次来北京吗？","Nǐmen shì dì-yī cì lái Běijīng ma","Is this your first time in Beijing?"),
    ("是的，我们都是第一次来。","Shì de wǒmen dōu shì dì-yī cì lái","Yes, it's the first time for both of us."),
    ("你们是来学中文的吗？","Nǐmen shì lái xué Zhōngwén de ma","Are you here to learn Chinese?"),
    ("不是，我们是来旅游的。","Bú shì wǒmen shì lái lǚyóu de","No, we're here for sightseeing."),
    ("我这几天都不忙，你们有事就找我。","Wǒ zhè jǐ tiān dōu bù máng nǐmen yǒu shì jiù zhǎo wǒ","I'm not busy these days—if you need anything, just come to me."),
    ("好的，谢谢您。","Hǎo de xièxie nín","Okay, thank you."),
  ]},
  {"name":"课文3 电话里请人帮忙","track":"1-5","sents":[
    ("喂，家月，你明天有时间吗？我想请你帮个忙。","Wèi Jiāyuè nǐ míngtiān yǒu shíjiān ma Wǒ xiǎng qǐng nǐ bāng gè máng","Hello, Jiayue, do you have time tomorrow? I'd like to ask you for a favor."),  # 呼语
    ("不好意思，天中，我已经到北京了。","Bù hǎoyìsi Tiānzhōng wǒ yǐjīng dào Běijīng le","Sorry, Tianzhong, I'm already in Beijing."),  # 呼语
    ("你是什么时候到的？","Nǐ shì shénme shíhou dào de","When did you get there?"),
    ("我是今天早上到的。你有事可以叫李文帮忙，他还在学校呢。","Wǒ shì jīntiān zǎoshang dào de Nǐ yǒu shì kěyǐ jiào Lǐ Wén bāngmáng tā hái zài xuéxiào ne","I arrived this morning. If you need anything, you can ask Li Wen for help—he's still at school."),
    ("好的，那我给他打个电话。","Hǎo de nà wǒ gěi tā dǎ gè diànhuà","Okay, then I'll give him a call."),
    ("好，再见！","Hǎo zàijiàn","All right, goodbye!"),
  ]},
  {"name":"课文4 酒店发信息（叙述体）","track":"1-7","sents":[
    ("王老师，我们已经到北京了，是您姐姐来接的我们。","Wáng lǎoshī wǒmen yǐjīng dào Běijīng le shì nín jiějie lái jiē de wǒmen","Ms. Wang, we've already arrived in Beijing—it was your sister who picked us up."),  # 呼语
    ("她请我们吃了北京烤鸭，还给我们介绍了很多东西。","Tā qǐng wǒmen chīle Běijīng Kǎoyā hái gěi wǒmen jièshàole hěn duō dōngxi","She treated us to Peking Duck and told us about many things."),
    ("我们的中文不太好，有时不太懂她的意思。","Wǒmen de Zhōngwén bú tài hǎo yǒushí bú tài dǒng tā de yìsi","Our Chinese isn't very good, so sometimes we don't quite understand what she means."),
  ]},
]},
{"id":"lesson-02","title":"还是打车去北大吧","en":"Let's take a taxi to Peking University instead","scenes":[
  {"name":"课文1 宾馆前台问路","track":"2-1","sents":[
    ("请问，这儿有到北京大学的公交车吗？","Qǐngwèn zhèr yǒu dào Běijīng Dàxué de gōngjiāochē ma","Excuse me, is there a bus from here to Peking University?"),
    ("有，但车站有点儿远。","Yǒu dàn chēzhàn yǒudiǎnr yuǎn","Yes, but the bus stop is a bit far."),
    ("这儿好打车吗？","Zhèr hǎo dǎchē ma","Is it easy to get a taxi around here?"),
    ("好打车。","Hǎo dǎchē","Yes, it's easy."),
    ("谢谢。安妮，我们还是打车去吧。","Xièxie Ānnī wǒmen háishi dǎchē qù ba","Thank you. Annie, let's take a taxi instead."),  # 呼语
    ("好，没问题。","Hǎo méi wèntí","Okay, no problem."),
  ]},
  {"name":"课文2 参观北大校园","track":"2-3","sents":[
    ("学校里人真多啊！","Xuéxiào li rén zhēn duō a","There are so many people on campus!"),
    ("是啊，北京大学有四万多名学生呢！","Shì a Běijīng Dàxué yǒu sìwàn duō míng xuéshēng ne","Yeah! Peking University has over forty thousand students!"),
    ("你是怎么知道的？","Nǐ shì zěnme zhīdào de","How do you know?"),
    ("是网上说的，网上还说北京大学有三千多名外国学生。","Shì wǎngshang shuō de wǎngshang hái shuō Běijīng Dàxué yǒu sānqiān duō míng wàiguó xuéshēng","I read it online—it also says Peking University has more than three thousand international students."),
    ("我也想来这儿学习。","Wǒ yě xiǎng lái zhèr xuéxí","I'd love to study here too."),
    ("那边就有一间教室，我们去看一下吧。","Nàbiān jiù yǒu yì jiān jiàoshì wǒmen qù kàn yíxià ba","There's a classroom right over there—let's go take a look."),
  ]},
  {"name":"课文3 校园里的电影院","track":"2-5","sents":[
    ("家月，你看，学校里有家电影院！","Jiāyuè nǐ kàn xuéxiào li yǒu jiā diànyǐngyuàn","Jiayue, look, there's a cinema on campus!"),  # 呼语
    ("是啊，电影院还不小。","Shì a diànyǐngyuàn hái bù xiǎo","Yeah, and it's not small either."),
    ("他们卖的电影票也很便宜。","Tāmen mài de diànyǐngpiào yě hěn piányi","The movie tickets they sell are really cheap too."),
    ("天啊！有的还不到二十块钱。","Tiān a Yǒude hái bú dào èrshí kuài qián","Goodness! Some are less than twenty yuan."),
    ("那你想不想去看个电影？","Nà nǐ xiǎng bu xiǎng qù kàn gè diànyǐng","So, do you want to go watch a movie?"),
    ("还是别看电影了，北京大学就很好看！","Háishi bié kàn diànyǐng le Běijīng Dàxué jiù hěn hǎokàn","Let's skip the movie—Peking University itself is well worth seeing!"),
  ]},
  {"name":"课文4 给天中发信息（叙述体）","track":"2-7","sents":[
    ("北京大学很大，有四万多名学生。","Běijīng Dàxué hěn dà yǒu sìwàn duō míng xuéshēng","Peking University is huge, with over forty thousand students."),
    ("学校很漂亮，里边还有家电影院，电影票也不贵，我们有时间还想再过来看个电影。","Xuéxiào hěn piàoliang lǐbian hái yǒu jiā diànyǐngyuàn diànyǐngpiào yě bú guì wǒmen yǒu shíjiān hái xiǎng zài guòlái kàn gè diànyǐng","The campus is beautiful, and there's even a cinema inside; the tickets aren't expensive, so when we have time we'd like to come back and watch a movie."),
  ]},
]},
{"id":"lesson-03","title":"我想去西安旅游","en":"I want to visit Xi'an","scenes":[
  {"name":"课文1 下班晚归到家","track":"3-1","sents":[
    ("今天回来这么晚啊！","Jīntiān huílái zhème wǎn a","You're back so late today!"),
    ("工作太多了，下班的时候没做完。","Gōngzuò tài duō le xiàbān de shíhou méi zuòwán","I had too much work and hadn't finished it by the time work ended."),
    ("菜都做好了，过来吃饭吧。","Cài dōu zuòhǎo le guòlái chī fàn ba","Dinner's all ready—come and eat."),
    ("我想休息一下，喝杯水。","Wǒ xiǎng xiūxi yíxià hē bēi shuǐ","I'd like to rest a bit and have a glass of water."),
    ("好的。","Hǎo de","Okay."),
  ]},
  {"name":"课文2 客厅商量去旅游","track":"3-3","sents":[
    ("我们找个时间去旅游，怎么样？","Wǒmen zhǎo gè shíjiān qù lǚyóu zěnmeyàng","How about we find some time to go on a trip?"),
    ("好啊，我也很想一起出去玩。","Hǎo a wǒ yě hěn xiǎng yìqǐ chūqù wán","Great! I've also been wanting to go out and have fun together."),
    ("你想去哪儿？","Nǐ xiǎng qù nǎr","Where do you want to go?"),
    ("我还没想好呢。","Wǒ hái méi xiǎnghǎo ne","I haven't decided yet."),
    ("那你再想一想，你想好了，我来买票。","Nà nǐ zài xiǎng yi xiǎng nǐ xiǎnghǎo le wǒ lái mǎi piào","Then think it over some more—once you've decided, I'll buy the tickets."),
  ]},
  {"name":"课文3 吃苹果提议去西安","track":"3-5","sents":[
    ("吃个苹果吧，我都洗好了。","Chī gè píngguǒ ba wǒ dōu xǐhǎo le","Have an apple—I've washed them all."),
    ("好的。","Hǎo de","Okay."),
    ("就在桌子上，你自己拿。","Jiù zài zhuōzi shang nǐ zìjǐ ná","They're right on the table—help yourself."),
    ("我去洗洗手。对了，我们去西安旅游，怎么样？","Wǒ qù xǐxi shǒu Duìle wǒmen qù Xī'ān lǚyóu zěnmeyàng","I'll go wash my hands. By the way, how about taking a trip to Xi'an?"),
    ("为什么想去西安？","Wèi shénme xiǎng qù Xī'ān","Why do you want to go to Xi'an?"),
    ("我看了看网上的介绍，这个时候去西安很不错！","Wǒ kànle kàn wǎngshang de jièshào zhège shíhou qù Xī'ān hěn búcuò","I read some introductions online—this is a great time to visit Xi'an!"),
  ]},
  {"name":"课文4 给好朋友打电话（叙述体）","track":"3-7","sents":[
    ("早上，刘明开车送孩子去学校，送完孩子回家后，医院就来电话了，让他回去上班。","Zǎoshang Liú Míng kāichē sòng háizi qù xuéxiào sòngwán háizi huí jiā hòu yīyuàn jiù lái diànhuà le ràng tā huíqù shàngbān","In the morning, Liu Ming drove the child to school, and just after he got home, the hospital called and asked him to go back to work."),
    ("我觉得他这个月每天都很累，真想让他休息休息。","Wǒ juéde tā zhège yuè měi tiān dōu hěn lèi zhēn xiǎng ràng tā xiūxi xiūxi","I feel he's been exhausted every day this month—I really wish he could get some rest."),
  ]},
]},
{"id":"lesson-04","title":"你穿红色的很好看","en":"You look pretty good in red","scenes":[
  {"name":"课文1 商场门口聊天","track":"4-1","sents":[
    ("妈妈，我们来过这家商场吗？","māma wǒ men lái guo zhè jiā shāng chǎng ma","Mom, have we been to this shopping mall before?"),  # 呼语
    ("没来过，这是新开的。","méi lái guo zhè shì xīn kāi de","No, we haven't. It just opened recently."),
    ("我们进去看看吧。","wǒ men jìn qù kàn kan ba","Let's go in and have a look."),
    ("好啊！你想买点儿什么？","hǎo a nǐ xiǎng mǎi diǎnr shén me","Sure! What do you want to buy?"),
    ("我想买条裤子。","wǒ xiǎng mǎi tiáo kù zi","I want to buy a pair of pants."),
    ("没问题。","méi wèn tí","No problem."),
  ]},
  {"name":"课文2 商场里看衣服","track":"4-3","sents":[
    ("妈妈，我想买这条白色的裤子。","māma wǒ xiǎng mǎi zhè tiáo bái sè de kù zi","Mom, I want to buy this pair of white pants."),  # 呼语
    ("你有很多白色的衣服，为什么还买白色的？","nǐ yǒu hěn duō bái sè de yī fu wèi shén me hái mǎi bái sè de","You already have lots of white clothes. Why buy white again?"),
    ("因为我喜欢白色啊！","yīn wèi wǒ xǐ huan bái sè a","Because I like white!"),
    ("我觉得这条白色的不太好看，你试试那条红色的吧。","wǒ jué de zhè tiáo bái sè de bú tài hǎo kàn nǐ shì shi nà tiáo hóng sè de ba","I don't think this white one looks very good. Why don't you try that red one?"),
    ("我没穿过红色的，红色的好看吗？","wǒ méi chuān guo hóng sè de hóng sè de hǎo kàn ma","I've never worn red before. Does red look good?"),
    ("就是因为没穿过，所以要试试啊！","jiù shì yīn wèi méi chuān guo suǒ yǐ yào shì shi a","That's exactly why you should give it a try!"),
  ]},
  {"name":"课文3 商场里挑书包","track":"4-5","sents":[
    ("妈妈，我想买个新书包。","māma wǒ xiǎng mǎi gè xīn shū bāo","Mom, I want to buy a new schoolbag."),  # 呼语
    ("好，那边卖书包，我们过去看看吧。","hǎo nà biān mài shū bāo wǒ men guò qù kàn kan ba","Okay. They sell schoolbags over there. Let's go take a look."),
    ("这么多漂亮的书包！","zhè me duō piào liang de shū bāo","So many beautiful schoolbags!"),
    ("红色的、绿色的、黑色的，你想买哪个？","hóng sè de lǜ sè de hēi sè de nǐ xiǎng mǎi nǎ ge","Red ones, green ones, black ones—which one do you want?"),
    ("绿色的吧。","lǜ sè de ba","The green one."),
    ("不错，我也觉得绿色的更好看。","bú cuò wǒ yě jué de lǜ sè de gèng hǎo kàn","Not bad. I think the green one looks better too."),
  ]},
  {"name":"课文4 小雪写日记（叙述体）","track":"4-7","sents":[
    ("我和妈妈去了一家商场。","wǒ hé mā ma qù le yì jiā shāng chǎng","I went to a shopping mall with my mom."),
    ("因为是新开的，所以这几天东西很便宜。","yīn wèi shì xīn kāi de suǒ yǐ zhè jǐ tiān dōng xi hěn pián yi","Since it just opened, things have been really cheap these days."),
    ("商场里的衣服颜色很多。","shāng chǎng li de yī fu yán sè hěn duō","The clothes in the mall come in many colors."),
    ("我没穿过红色的裤子，妈妈让我试了试，我觉得我穿红色的也很好看。","wǒ méi chuān guo hóng sè de kù zi mā ma ràng wǒ shì le shì wǒ jué de wǒ chuān hóng sè de yě hěn hǎo kàn","I had never worn red pants before, but my mom had me try them on, and I thought I looked pretty good in red too."),
  ]},
]},
{"id":"lesson-05","title":"第一次去中国朋友家","en":"Visiting a Chinese friend's home for the first time","scenes":[
  {"name":"课文1 宾馆楼下打电话","track":"5-1","sents":[
    ("家月，快下来吧，第一次去中国朋友家，别晚了。","jiā yuè kuài xià lái ba dì yī cì qù zhōng guó péng you jiā bié wǎn le","Jiayue, come down quickly. It's our first time visiting a Chinese friend's home—don't be late."),  # 呼语
    ("还有时间，你上来吧。","hái yǒu shí jiān nǐ shàng lái ba","We still have time. Why don't you come up?"),
    ("我不上去了，就在下面等你。","wǒ bú shàng qù le jiù zài xià miàn děng nǐ","I'm not going up. I'll just wait for you downstairs."),
    ("那我一会儿就下去。","nà wǒ yí huìr jiù xià qù","Then I'll come down in a bit."),
    ("你快点儿吧。","nǐ kuài diǎnr ba","Hurry up."),
    ("没事，一雪姐说十一点前到就可以。","méi shì yī xuě jiě shuō shí yī diǎn qián dào jiù kě yǐ","It's fine. Sister Yixue said we just need to arrive before eleven."),  # 原文印"11"
  ]},
  {"name":"课文2 到王一雪家做客","track":"5-3","sents":[
    ("家月、安妮，快进来！我给你们介绍一下，这是孩子们的爷爷、奶奶。","jiā yuè ān nī kuài jìn lái wǒ gěi nǐ men jiè shào yí xià zhè shì hái zi men de yé ye nǎi nai","Jiayue, Annie, come on in! Let me introduce you—these are the children's grandfather and grandmother."),  # 呼语
    ("你们好！","nǐ men hǎo","Hello!"),
    ("爸，妈，这是白家月，这是安妮。她们都是一飞的学生。","bà mā zhè shì bái jiā yuè zhè shì ān nī tā men dōu shì yī fēi de xué shēng","Dad, Mom, this is Bai Jiayue, and this is Annie. They're both Yifei's students."),  # 呼语
    ("家月、安妮，你们好！","jiā yuè ān nī nǐ men hǎo","Hello, Jiayue and Annie!"),  # 呼语
    ("这是送你们的礼物。","zhè shì sòng nǐ men de lǐ wù","These are gifts for you."),
    ("你们太客气了，还拿这么多礼物来！","nǐ men tài kè qi le hái ná zhè me duō lǐ wù lái","You're too kind—bringing so many gifts!"),
    ("一雪姐，这是给孩子们准备的礼物。","yī xuě jiě zhè shì gěi hái zi men zhǔn bèi de lǐ wù","Sister Yixue, this is the gift we prepared for the children."),  # 呼语
    ("谢谢！你们别客气，快坐吧！","xiè xie nǐ men bié kè qi kuài zuò ba","Thank you! Make yourselves at home—please, have a seat!"),
  ]},
  {"name":"课文3 王一雪家吃饭","track":"5-5","sents":[
    ("都十二点了，我们吃饭吧。","dōu shí èr diǎn le wǒ men chī fàn ba","It's already twelve o'clock. Let's eat."),  # 原文印"12"
    ("这么多好吃的，您太客气了！","zhè me duō hǎo chī de nín tài kè qi le","So many delicious dishes—you're really too kind!"),
    ("都是我自己做的，你们多吃点儿。","dōu shì wǒ zì jǐ zuò de nǐ men duō chī diǎnr","I made all of these myself. Please eat as much as you like."),
    ("奶茶也很好喝，是您自己做的吗？","nǎi chá yě hěn hǎo hē shì nín zì jǐ zuò de ma","The bubble tea is delicious too. Did you make it yourself?"),
    ("不是，奶茶是爷爷买的。","bú shì nǎi chá shì yé ye mǎi de","No, Grandpa bought the bubble tea."),
    ("在哪儿买的？我还没喝过这么好喝的奶茶。","zài nǎr mǎi de wǒ hái méi hē guo zhè me hǎo hē de nǎi chá","Where did he buy it? I've never had bubble tea this good before."),
    ("就在前边的商场，吃完饭你们可以跟我去看看。","jiù zài qián bian de shāng chǎng chī wán fàn nǐ men kě yǐ gēn wǒ qù kàn kan","At the mall just up ahead. After we finish eating, you can come with me to check it out."),
  ]},
  {"name":"课文4 宾馆里发信息（叙述体）","track":"5-7","sents":[
    ("回国前一天，我们去一雪姐家了。","huí guó qián yì tiān wǒ men qù yī xuě jiě jiā le","The day before we returned to our countries, we visited Sister Yixue's home."),
    ("到她家的时候，饭菜都做好了。","dào tā jiā de shí hou fàn cài dōu zuò hǎo le","When we arrived, the food was already prepared."),
    ("刘爷爷还准备了奶茶。","liú yé ye hái zhǔn bèi le nǎi chá","Grandpa Liu had even prepared bubble tea."),
    ("因为吃了太多东西，我们吃完饭是走回酒店的。","yīn wèi chī le tài duō dōng xi wǒ men chī wán fàn shì zǒu huí jiǔ diàn de","Because we ate so much, we walked back to the hotel after the meal."),
  ]},
]},
{"id":"lesson-06","title":"小雪，生日快乐！","en":"Happy birthday, Xiaoxue!","scenes":[
  {"name":"课文1 在家商量生日礼物","track":"6-1","sents":[
    ("明天就是女儿的生日了。","míng tiān jiù shì nǚ ér de shēng rì le","Tomorrow is our daughter's birthday."),
    ("你不说，我还真忘了。我们给她准备个什么礼物呢？","nǐ bù shuō wǒ hái zhēn wàng le wǒ men gěi tā zhǔn bèi gè shén me lǐ wù ne","If you hadn't mentioned it, I would have completely forgotten. What gift should we prepare for her?"),
    ("她喜欢画画，你觉得画笔怎么样？","tā xǐ huan huà huà nǐ jué de huà bǐ zěn me yàng","She likes drawing. How about some color pens?"),
    ("就送画笔吧！","jiù sòng huà bǐ ba","Let's give her color pens then!"),
    ("那我明天上午就去买。","nà wǒ míng tiān shàng wǔ jiù qù mǎi","Then I'll go buy them tomorrow morning."),
    ("好的！我再给她买个大大的生日蛋糕。","hǎo de wǒ zài gěi tā mǎi gè dà dà de shēng rì dàn gāo","Great! And I'll also buy her a great big birthday cake."),
  ]},
  # ⚠️ 本篇 8 句全部手工钉死 clip 区间。原因: 整篇是生日祝福,句式高度重复
  #（「小雪，生日快乐！」→「姐姐，生日快乐！」→「小雪，这是…」),相邻句首尾撞词,
  # ASR 的 DP 对齐会整体挪位且分数照样很高(实测: 第2句多吃下句的「小雪」、第3句缺开头、
  # 第5句丢了「画笔」),**靠分数看不出来,只能人工定界**。
  # 区间取自 6-3.mp3 的 gap0.35 静音分段(seg 编号见下),按段内容与课文逐句核对得出。
  {"name":"课文2 生日送礼物","track":"6-3","sents":[
    ("小雪，生日快乐！","xiǎo xuě shēng rì kuài lè","Happy birthday, Xiaoxue!", {"clip":(0.68, 2.42)}),  # 呼语 seg0+1
    ("姐姐，生日快乐！","jiě jie shēng rì kuài lè","Happy birthday, sis!", {"clip":(3.80, 5.16)}),  # 呼语 seg2
    ("小雪，这是爸爸、妈妈送你的礼物。","xiǎo xuě zhè shì bà ba mā ma sòng nǐ de lǐ wù","Xiaoxue, here's a gift from Dad and Mom.", {"clip":(6.35, 10.09)}),  # 呼语 seg3+4
    ("你打开看看喜欢不喜欢。","nǐ dǎ kāi kàn kan xǐ huan bu xǐ huan","Open it and see if you like it.", {"clip":(11.39, 13.64)}),  # seg5
    ("画笔！我很喜欢！","huà bǐ wǒ hěn xǐ huan","Color pens! I love them!", {"clip":(14.93, 17.01)}),  # seg6+7
    ("那你想画点儿什么？","nà nǐ xiǎng huà diǎnr shén me","So what would you like to draw?", {"clip":(18.22, 19.57)}),  # seg8
    ("画我们的家！有爸爸、妈妈、弟弟，还有黑色的狗、白色的猫什么的。","huà wǒ men de jiā yǒu bà ba mā ma dì di hái yǒu hēi sè de gǒu bái sè de māo shén me de","Our home! With Dad, Mom, my little brother, plus our black dog, white cat, and so on.", {"clip":(20.59, 28.33)}),  # seg9-13
    ("那我要画一个穿白色衣服的姐姐。","nà wǒ yào huà yí gè chuān bái sè yī fu de jiě jie","Then I'll draw a big sister wearing white clothes.", {"clip":(29.34, 31.68)}),  # seg14
  ]},
  {"name":"课文3 客厅里过生日","track":"6-5","sents":[
    ("小雪，看看今天有什么好吃的。","xiǎo xuě kàn kan jīn tiān yǒu shén me hǎo chī de","Xiaoxue, take a look at all the delicious food we have today."),  # 呼语
    ("长长的面条儿，大大的蛋糕。","cháng cháng de miàn tiáor dà dà de dàn gāo","Long, long noodles and a great big cake."),
    ("你看，还有鱼啊肉啊什么的，都是你喜欢吃的。","nǐ kàn hái yǒu yú a ròu a shén me de dōu shì nǐ xǐ huan chī de","Look, there's also fish, meat, and more—all your favorites."),
    ("谢谢爸爸、妈妈！","xiè xie bà ba mā ma","Thank you, Dad and Mom!"),
    ("快去叫弟弟过来吃饭吧，吃完饭我们还要出去玩呢。","kuài qù jiào dì di guò lái chī fàn ba chī wán fàn wǒ men hái yào chū qù wán ne","Go call your little brother over to eat. After dinner we're going out to have some fun!"),
    ("过生日真好啊！","guò shēng rì zhēn hǎo a","Birthdays are so wonderful!"),
    ("是的，过生日就要吃好吃的，还要高高兴兴地玩。","shì de guò shēng rì jiù yào chī hǎo chī de hái yào gāo gāo xìng xìng de wán","That's right! On your birthday you should eat delicious food and play to your heart's content."),
  ]},
  {"name":"课文4 一雪写日记（叙述体）","track":"6-7","sents":[
    ("今天是女儿的生日。","jīn tiān shì nǚ ér de shēng rì","Today was our daughter's birthday."),
    ("我们买了蛋糕，做了面条儿，还做了鱼啊肉啊什么的。","wǒ men mǎi le dàn gāo zuò le miàn tiáor hái zuò le yú a ròu a shén me de","We bought a cake, made noodles, and also cooked fish, meat, and other dishes."),
    ("吃完晚饭，一家人去看了个电影。","chī wán wǎn fàn yì jiā rén qù kàn le gè diàn yǐng","After dinner, the whole family went to watch a movie."),
    ("回家后，孩子们早早地就上床了。","huí jiā hòu hái zi men zǎo zǎo de jiù shàng chuáng le","After we got home, the children went to bed early."),
    ("明天不上学，他们说要舒舒服服地睡一觉，让我们晚点儿叫他们起床。","míng tiān bú shàng xué tā men shuō yào shū shū fú fú de shuì yí jiào ràng wǒ men wǎn diǎnr jiào tā men qǐ chuáng","There's no school tomorrow, so they said they wanted to sleep soundly and comfortably, and asked us to wake them up a bit later."),
    ("这是很忙、很累，但很快乐的一天。","zhè shì hěn máng hěn lèi dàn hěn kuài lè de yì tiān","It was a busy and tiring day, but a very happy one."),
  ]},
]},
{"id":"lesson-07","title":"他篮球打得很好","en":"He plays basketball very well","scenes":[
  {"name":"课文1 下课去打篮球","track":"7-1","sents":[
    ("安妮，你是什么时候从北京回来的？","Ānnī nǐ shì shénme shíhou cóng Běijīng huílái de","Annie, when did you get back from Beijing?"),  # 呼语
    ("昨天下午。天中，你怎么一下课就往外跑？","zuótiān xiàwǔ Tiānzhōng nǐ zěnme yí xiàkè jiù wǎng wài pǎo","Yesterday afternoon. Tianzhong, why do you rush out as soon as class ends?"),
    ("我跟同学说好了，一起去打篮球。","wǒ gēn tóngxué shuōhǎo le yìqǐ qù dǎ lánqiú","I made plans with my classmates to play basketball together."),
    ("我也想跟你们一起玩。","wǒ yě xiǎng gēn nǐmen yìqǐ wán","I want to join you too."),
    ("没问题，走吧。","méi wèntí zǒu ba","No problem, let's go."),
  ]},
  {"name":"课文2 喜欢的运动","track":"7-3","sents":[
    ("天中，你是不是很喜欢打篮球？","Tiānzhōng nǐ shì bu shì hěn xǐhuan dǎ lánqiú","Tianzhong, do you really like playing basketball?"),  # 呼语
    ("没错。","méi cuò","That's right."),
    ("你还喜欢什么运动？","nǐ hái xǐhuan shénme yùndòng","What other sports do you like?"),
    ("我还喜欢踢足球，一到星期天就跟朋友们去踢球。","wǒ hái xǐhuan tī zúqiú yí dào Xīngqītiān jiù gēn péngyoumen qù tī qiú","I also like playing soccer; every Sunday I go play with my friends."),
    ("你踢得怎么样？","nǐ tī de zěnmeyàng","How well do you play?"),
    ("我踢得还可以。","wǒ tī de hái kěyǐ","I play okay."),
  ]},
  {"name":"课文3 跑步和游泳","track":"7-5","sents":[
    ("你篮球打得怎么样？","nǐ lánqiú dǎ de zěnmeyàng","How are your basketball skills?"),
    ("打得还可以。","dǎ de hái kěyǐ","Not too bad."),
    ("跑步呢？你跑得快不快？","pǎobù ne nǐ pǎo de kuài bu kuài","What about running? Are you fast?"),
    ("我跑得不快，也不太喜欢跑步。","wǒ pǎo de bú kuài yě bú tài xǐhuan pǎobù","I'm not fast, and I don't really like running either."),
    ("那你喜欢游泳吗？","nà nǐ xǐhuan yóuyǒng ma","Do you like swimming, then?"),
    ("喜欢，但我游泳游得不快。","xǐhuan dàn wǒ yóuyǒng yóu de bú kuài","I do, but I don't swim very fast."),
  ]},
  {"name":"课文4 我的爱好是运动（叙述体）","track":"7-7","sents":[
    ("我的爱好是运动。","wǒ de àihào shì yùndòng","My hobby is doing sports."),
    ("从上小学开始，我每天都跟爸爸去运动。","cóng shàng xiǎoxué kāishǐ wǒ měi tiān dōu gēn bàba qù yùndòng","Since primary school, I've been exercising with my dad every day."),
    ("现在我篮球打得很好，足球踢得不错，游泳游得也很快。","xiànzài wǒ lánqiú dǎ de hěn hǎo zúqiú tī de búcuò yóuyǒng yóu de yě hěn kuài","Now I play basketball very well, play soccer quite well, and swim very fast too."),
    ("我一有时间就去运动。","wǒ yì yǒu shíjiān jiù qù yùndòng","Whenever I have time, I go do sports."),
  ]},
]},
{"id":"lesson-08","title":"虽然你忘了，但是我记得","en":"Even though you forgot, I remembered","scenes":[
  {"name":"课文1 商场挑手表","track":"8-1","sents":[
    ("你看，这两块手表怎么样？","nǐ kàn zhè liǎng kuài shǒubiǎo zěnmeyàng","Look, what do you think of these two watches?"),
    ("都不错！","dōu búcuò","They're both nice!"),
    ("我喜欢左边这个。","wǒ xǐhuan zuǒbian zhège","I like the one on the left."),
    ("我也觉得左边的比右边的好看。","wǒ yě juéde zuǒbian de bǐ yòubian de hǎokàn","I also think the left one looks better than the right one."),
    ("你看看要多少钱！","nǐ kànkan yào duōshao qián","Check how much it costs!"),
    ("真不便宜！八千八！","zhēn bù piányi bā qiān bā","It's really not cheap! 8,800!"),
  ]},
  {"name":"课文2 电影院选电影","track":"8-3","sents":[
    ("今天有不少电影，我们看个电影吧。","jīntiān yǒu bù shǎo diànyǐng wǒmen kàn gè diànyǐng ba","There are quite a few movies today. Let's watch one."),
    ("好啊！我们看哪个？","hǎo a wǒmen kàn nǎge","Great! Which one should we watch?"),
    ("我记得你喜欢看爱情片，我们看那个爱情片，怎么样？","wǒ jìde nǐ xǐhuan kàn àiqíngpiàn wǒmen kàn nàge àiqíngpiàn zěnmeyàng","I remember you like romantic movies. How about that romantic one?"),
    ("还是看这个吧，我看网上说这个电影比那个爱情片更有意思。","háishi kàn zhège ba wǒ kàn wǎngshang shuō zhège diànyǐng bǐ nàge àiqíngpiàn gèng yǒu yìsi","Let's watch this one instead — I read online that it's more interesting than that romantic one."),
    ("好。我去买票。","hǎo wǒ qù mǎi piào","Okay. I'll go buy the tickets."),
    ("到网上买吧，网上买比在这里买便宜。","dào wǎngshang mǎi ba wǎngshang mǎi bǐ zài zhèlǐ mǎi piányi","Buy them online — it's cheaper online than here."),
  ]},
  {"name":"课文3 饭馆生日惊喜","track":"8-5","sents":[
    ("您好！就要这几个菜吧，谢谢！","nín hǎo jiù yào zhè jǐ gè cài ba xièxie","Hello! We'll have these dishes, thank you!"),
    ("怎么点这么多菜？","zěnme diǎn zhème duō cài","Why did you order so many dishes?"),
    ("你想想，今天是几月几号？","nǐ xiǎngxiang jīntiān shì jǐ yuè jǐ hào","Think about it — what's the date today?"),
    # ⚠️ clip 手工钉死: 下一句以「生日快乐！」开头,与本句尾「我的生日」撞词,ASR 对齐多吃了一段。
    # 区间取自 8-5.mp3 gap0.35 分段 seg5+seg6+seg7
    ("八月二十七号。啊！我的生日！","bā yuè èrshíqī hào à wǒ de shēngrì","August 27th. Ah! My birthday!", {"clip":(11.95, 15.04)}),  # 原文印"8月27号"
    ("生日快乐！虽然你忘了，但是我记得。看看这是什么？","shēngrì kuàilè suīrán nǐ wàng le dànshì wǒ jìde kànkan zhè shì shénme","Happy birthday! Even though you forgot, I remembered. Look, what's this?"),
    ("手表！吃饭、看电影、买手表，今天花了不少钱吧？","shǒubiǎo chī fàn kàn diànyǐng mǎi shǒubiǎo jīntiān huāle bù shǎo qián ba","The watch! Dinner, a movie, and the watch — you must have spent a lot today, right?"),
    ("虽然花了一些钱，但是我们过了一个快乐的生日。","suīrán huāle yìxiē qián dànshì wǒmen guòle yí gè kuàilè de shēngrì","Although we spent some money, we celebrated a happy birthday."),
  ]},
  {"name":"课文4 丈夫记得生日（叙述体）","track":"8-7","sents":[
    ("虽然妻子忘了今天是自己的生日，但是丈夫记得。","suīrán qīzi wàngle jīntiān shì zìjǐ de shēngrì dànshì zhàngfu jìde","Although the wife forgot that today was her own birthday, the husband remembered."),
    ("丈夫请妻子去饭馆吃饭、去电影院看电影，还给妻子买了一块非常漂亮的手表。","zhàngfu qǐng qīzi qù fànguǎn chī fàn qù diànyǐngyuàn kàn diànyǐng hái gěi qīzi mǎile yí kuài fēicháng piàoliang de shǒubiǎo","The husband treated his wife to a meal at a restaurant and a movie at the cinema, and also bought her a very beautiful watch."),
    ("妻子觉得今天很快乐。","qīzi juéde jīntiān hěn kuàilè","The wife felt very happy today."),
  ]},
]},
{"id":"lesson-09","title":"我去买杯奶茶","en":"I'm going to buy a cup of bubble tea","scenes":[
  {"name":"课文1 商店买裤子","track":"9-1","sents":[
    ("儿子的裤子坏了，我们给他买条新的吧。","érzi de kùzi huài le wǒmen gěi tā mǎi tiáo xīn de ba","Our son's pants are ruined. Let's buy him a new pair."),
    ("好啊。","hǎo a","Okay."),
    ("你看这条黑色的怎么样？","nǐ kàn zhè tiáo hēisè de zěnmeyàng","What do you think of this black pair?"),
    ("没有你上次买的那条好看。","méiyǒu nǐ shàng cì mǎi de nà tiáo hǎokàn","They're not as nice as the pair you bought last time."),
    ("旁边那个男孩儿就穿了这样的裤子，我觉得很好看啊！","pángbiān nàge nánháir jiù chuānle zhèyàng de kùzi wǒ juéde hěn hǎokàn a","The boy next to us is wearing pants just like these, and I think they look great!"),
    ("儿子的个子没有他那么高，穿上就不会太好看。","érzi de gèzi méiyǒu tā nàme gāo chuānshàng jiù bú huì tài hǎokàn","Our son isn't as tall as him, so they wouldn't look so good on him."),
    ("好吧，我们再去那边看看。","hǎo ba wǒmen zài qù nàbiān kànkan","Alright, let's go over there and take another look."),
  ]},
  {"name":"课文2 买奶茶喝咖啡","track":"9-3","sents":[
    ("门口有家奶茶店。你想喝杯奶茶吗？","ménkǒu yǒu jiā nǎichádiàn nǐ xiǎng hē bēi nǎichá ma","There's a bubble tea shop at the entrance. Do you want a cup of bubble tea?"),
    ("我想喝咖啡，还是去咖啡店吧。","wǒ xiǎng hē kāfēi háishi qù kāfēidiàn ba","I'd rather have coffee — let's go to a coffee shop."),
    ("咖啡店离这儿有点儿远。","kāfēidiàn lí zhèr yǒudiǎnr yuǎn","The coffee shop is a bit far from here."),
    ("没关系，那家店的咖啡很好喝。","méi guānxi nà jiā diàn de kāfēi hěn hǎo hē","That's fine — that shop's coffee is really good."),
    ("那你等一下，我去买杯奶茶。","nà nǐ děng yíxià wǒ qù mǎi bēi nǎichá","Then wait a moment — I'll go buy a cup of bubble tea."),
    ("你不想喝咖啡吗？","nǐ bù xiǎng hē kāfēi ma","Don't you want coffee?"),
    ("喝了咖啡，晚上就别想睡觉了。","hēle kāfēi wǎnshang jiù bié xiǎng shuìjiào le","If I drink coffee, I can forget about sleeping tonight."),
  ]},
  {"name":"课文3 走路回家运动","track":"9-5","sents":[
    ("我们打车回去吧。","wǒmen dǎchē huíqù ba","Let's take a taxi home."),
    ("这里离家很近，还是走路吧。","zhèlǐ lí jiā hěn jìn háishi zǒulù ba","It's very close to home from here — let's walk instead."),
    ("要走多长时间？","yào zǒu duō cháng shíjiān","How long will the walk take?"),
    ("走半个多小时就到了。","zǒu bàn gè duō xiǎoshí jiù dào le","A little over half an hour and we'll be there."),
    ("好的。每天上下班都坐车，今天运动运动吧。","hǎo de měi tiān shàng xià bān dōu zuò chē jīntiān yùndòng yùndòng ba","Alright. I ride to and from work every day — let's get some exercise today."),
  ]},
  {"name":"课文4 日记记逛街一天（叙述体）","track":"9-7","sents":[
    ("这周刘明休息，我下班后跟他去了一家商店。","zhè zhōu Liú Míng xiūxi wǒ xiàbān hòu gēn tā qùle yì jiā shāngdiàn","Liu Ming is off this week, so I went to a store with him after work."),
    ("商店里边的衣服没有大商场里的好看。","shāngdiàn lǐbian de yīfu méiyǒu dà shāngchǎng li de hǎokàn","The clothes in the store weren't as nice as those in big shopping malls."),
    ("我们没有买到喜欢的衣服，从商店出来就到咖啡店坐了坐。","wǒmen méiyǒu mǎidào xǐhuan de yīfu cóng shāngdiàn chūlái jiù dào kāfēidiàn zuòle zuò","We didn't find any clothes we liked, so after leaving the store we sat for a while at a coffee shop."),
    ("因为想运动运动，所以喝完东西，我们就走回家了。","yīnwèi xiǎng yùndòng yùndòng suǒyǐ hēwán dōngxi wǒmen jiù zǒuhuí jiā le","Since we wanted to get some exercise, we walked home after finishing our drinks."),
  ]},
]},
{"id":"lesson-10","title":"就要考试了","en":"The exam is coming","scenes":[
  {"name":"课文1 帮儿子备开学","track":"10-1","sents":[
    ("小明，你们明天开学，你准备好了吗？","Xiǎomíng, nǐmen míngtiān kāixué, nǐ zhǔnbèi hǎo le ma?","Xiaoming, school starts tomorrow. Are you ready?"),  # 呼语
    ("明天就开学啊？爸爸，我的书包你看见了吗？","Míngtiān jiù kāixué a? Bàba, wǒ de shūbāo nǐ kànjiànle ma?","School starts tomorrow already? Dad, have you seen my schoolbag?"),
    ("书包在门后面。","Shūbāo zài mén hòumiàn.","The schoolbag is behind the door."),
    ("书在哪儿呢？笔呢？","Shū zài nǎr ne? Bǐ ne?","Where are the books? And the pens?"),
    ("书在床上，笔在桌子上。","Shū zài chuáng shang, bǐ zài zhuōzi shang.","The books are on the bed, and the pens are on the table."),
    ("太好了！现在都准备好了。","Tài hǎo le! Xiànzài dōu zhǔnbèi hǎo le.","Great! Everything is ready now."),
    ("这次爸爸帮你，下次你自己准备，好不好？","Zhè cì bàba bāng nǐ, xià cì nǐ zìjǐ zhǔnbèi, hǎo bu hǎo?","Dad helped you this time. Next time you prepare by yourself, okay?"),
    ("好！","Hǎo!","Okay!"),
  ]},
  {"name":"课文2 考前看书复习","track":"10-3","sents":[
    ("小雪，你在做什么呢？","Xiǎoxuě, nǐ zài zuò shénme ne?","Xiaoxue, what are you doing?"),  # 呼语
    ("明天考试，我在看书呢。","Míngtiān kǎoshì, wǒ zài kàn shū ne.","I have an exam tomorrow, so I'm reading."),
    ("这些词要好好看看。","Zhèxiē cí yào hǎohǎo kànkan.","You should review these words carefully."),
    ("我看过了，意思也都懂了。","Wǒ kànguo le, yìsi yě dōu dǒng le.","I've reviewed them, and I understand all their meanings."),
    ("你的本子呢？本子上做错的题也要看一看。","Nǐ de běnzi ne? Běnzi shang zuòcuò de tí yě yào kàn yi kàn.","Where's your notebook? You should also go over the questions you got wrong in it."),
    ("妈妈，是您准备考试还是我准备考试？","Māma, shì nín zhǔnbèi kǎoshì háishi wǒ zhǔnbèi kǎoshì?","Mom, are you the one preparing for the exam or am I?"),  # 呼语
  ]},
  {"name":"课文3 考后回家聊成绩","track":"10-5","sents":[
    ("妈妈，我回来了！","Māma, wǒ huílái le!","Mom, I'm back!"),  # 呼语
    ("我买了奶茶，就在桌子上，自己去拿吧。","Wǒ mǎile nǎichá, jiù zài zhuōzi shang, zìjǐ qù ná ba.","I bought bubble tea; it's on the table. Go get it yourself."),
    ("谢谢妈妈！","Xièxie māma!","Thank you, Mom!"),
    ("今天考试考得怎么样？","Jīntiān kǎoshì kǎo de zěnmeyàng?","How did your exam go today?"),
    ("我觉得比上次好。","Wǒ juéde bǐ shàng cì hǎo.","I think I did better than last time."),
    ("真不错！饭菜快要做好了，你叫弟弟一起去洗手吧。","Zhēn búcuò! Fàncài kuàiyào zuòhǎo le, nǐ jiào dìdi yìqǐ qù xǐshǒu ba.","Really good! The food is almost ready. Go ask your little brother to wash hands with you."),
    ("妈妈，我是第一名，姐姐还没洗完呢。","Māma, wǒ shì dì-yī míng, jiějie hái méi xǐwán ne.","Mom, I finished first — my sister hasn't finished washing yet."),  # 呼语；此句前教材印「……」
    ("你洗得真快啊！","Nǐ xǐ de zhēn kuài a!","You washed so quickly!"),
  ]},
  {"name":"课文4 日记·全家备开学备考（叙述体）","track":"10-7","sents":[
    ("快要开学了，爸爸帮弟弟准备书包、本子和笔。","Kuàiyào kāixué le, bàba bāng dìdi zhǔnbèi shūbāo běnzi hé bǐ.","School is about to start, and Dad is helping my younger brother prepare his schoolbag, notebooks, and pens."),
    ("我就要考试了，妈妈让我看书、看做错的题。","Wǒ jiù yào kǎoshì le, māma ràng wǒ kàn shū kàn zuòcuò de tí.","I'm about to take an exam, and Mom asked me to read my books and review the questions I got wrong."),
    ("我们上学，爸爸、妈妈比我们还忙。","Wǒmen shàngxué, bàba māma bǐ wǒmen hái máng.","When we go to school, Mom and Dad are even busier than we are."),
    ("我问他们：“是我和弟弟上学还是你们上学？”","Wǒ wèn tāmen Shì wǒ hé dìdi shàngxué háishi nǐmen shàngxué","I asked them, \"Is it my brother and me going to school, or is it you?\""),
    ("我问完，他们都笑了。","Wǒ wènwán, tāmen dōu xiào le.","After I asked, they both laughed."),
  ]},
]},
{"id":"lesson-11","title":"我最喜欢吃中国菜","en":"I like Chinese food the most","scenes":[
  {"name":"课文1 教室里头疼","track":"11-1","sents":[
    ("家月，都下课了，你怎么还不回家？","Jiāyuè, dōu xiàkè le, nǐ zěnme hái bù huí jiā?","Jiayue, class is over. Why haven't you gone home yet?"),  # 呼语
    ("我头疼，不太舒服。","Wǒ tóu téng, bú tài shūfu.","I have a headache; I'm not feeling well."),
    ("你这几天经常头疼，去医院看看吧。","Nǐ zhè jǐ tiān jīngcháng tóu téng, qù yīyuàn kànkan ba.","You've been having headaches frequently these days. You should go to the hospital."),
    ("我想休息一下，现在不能动，一动就疼。","Wǒ xiǎng xiūxi yíxià, xiànzài bù néng dòng, yí dòng jiù téng.","I want to rest for a while. I can't move right now — it hurts whenever I move."),
    ("那你在这儿坐着，我去开车，一会儿送你去医院。","Nà nǐ zài zhèr zuòzhe, wǒ qù kāichē, yíhuìr sòng nǐ qù yīyuàn.","Then sit here. I'll go get the car and take you to the hospital in a bit."),
    ("谢谢王老师。","Xièxie Wáng lǎoshī.","Thank you, Ms. Wang."),
  ]},
  {"name":"课文2 车上接李文电话","track":"11-3","sents":[
    ("现在路上车多，还下着雪，我开慢一点儿。","Xiànzài lùshang chē duō, hái xiàzhe xuě, wǒ kāi màn yìdiǎnr.","There are a lot of cars on the road now, and it's snowing. I'll drive a bit slower."),
    ("没问题，现在头没那么疼了。","Méi wèntí, xiànzài tóu méi nàme téng le.","No problem. My head doesn't hurt as much now."),
    ("好。李文来电话了，你帮我接一下。","Hǎo. Lǐ Wén lái diànhuà le, nǐ bāng wǒ jiē yíxià.","Okay. Li Wen is calling — please answer it for me."),
    ("喂，李文，王老师开着车呢，你找她有事吗？","Wèi, Lǐ Wén, Wáng lǎoshī kāizhe chē ne, nǐ zhǎo tā yǒu shì ma?","Hello, Li Wen. Ms. Wang is driving. Do you need her for something?"),  # 呼语
    ("没什么事。今天雪这么大，你们开车去哪儿啊？","Méi shénme shì. Jīntiān xuě zhème dà, nǐmen kāichē qù nǎr a?","Nothing important. The snow is so heavy today — where are you driving to?"),
    ("去医院，我头有点儿疼。","Qù yīyuàn, wǒ tóu yǒudiǎnr téng.","To the hospital. I have a bit of a headache."),
    ("那我一会儿去看看你。","Nà wǒ yíhuìr qù kànkan nǐ.","Then I'll come visit you in a while."),
  ]},
  {"name":"课文3 探病·做中国菜","track":"11-5","sents":[
    ("李文，快请进！","Lǐ Wén, kuài qǐng jìn!","Li Wen, please come in!"),  # 呼语
    ("家月，你怎么样了？头还疼吗？","Jiāyuè, nǐ zěnmeyàng le? Tóu hái téng ma?","Jiayue, how are you feeling? Does your head still hurt?"),  # 呼语
    ("不那么疼了。医生开了一些药，吃完就好多了。","Bú nàme téng le. Yīshēng kāile yìxiē yào, chīwán jiù hǎoduō le.","It doesn't hurt as much. The doctor prescribed some medicine, and I felt much better after taking it."),
    ("那就好！","Nà jiù hǎo!","That's good to hear!"),
    ("家月，你想不想吃点儿东西？","Jiāyuè, nǐ xiǎng bu xiǎng chī diǎnr dōngxi?","Jiayue, do you want something to eat?"),  # 呼语
    ("吃点儿吧，身体不舒服时更要好好吃饭。","Chī diǎnr ba, shēntǐ bù shūfu shí gèng yào hǎohǎo chī fàn.","Eat something. You should eat well especially when you're not feeling well."),
    ("吃点儿什么呢？","Chī diǎnr shénme ne?","What should I eat?"),
    ("你最喜欢吃中国菜，我做几个中国菜吧。","Nǐ zuì xǐhuan chī Zhōngguó cài, wǒ zuò jǐ gè Zhōngguó cài ba.","You like Chinese food the most, so I'll cook a few Chinese dishes."),
    ("好的，谢谢王老师。","Hǎo de, xièxie Wáng lǎoshī.","Okay, thank you, Ms. Wang."),
  ]},
  {"name":"课文4 日记·头疼去医院（叙述体）","track":"11-7","sents":[
    ("我这几天经常头疼，从药店买了点儿药，没去医院。","Wǒ zhè jǐ tiān jīngcháng tóu téng, cóng yàodiàn mǎile diǎnr yào, méi qù yīyuàn.","I've been having frequent headaches these days; I bought some medicine at the pharmacy and didn't go to the hospital."),
    ("今天下课后，王老师看我不舒服，就送我去医院了。","Jīntiān xiàkè hòu, Wáng lǎoshī kàn wǒ bù shūfu, jiù sòng wǒ qù yīyuàn le.","After class today, Ms. Wang saw that I wasn't feeling well and took me to the hospital."),
    ("从医院回来，李文也来看我了。","Cóng yīyuàn huílái, Lǐ Wén yě lái kàn wǒ le.","After I got back from the hospital, Li Wen also came to see me."),
    ("现在他们都回去了，我也要睡觉了。","Xiànzài tāmen dōu huíqù le, wǒ yě yào shuìjiào le.","Now they've all gone home, and I'm going to bed too."),
  ]},
]},
{"id":"lesson-12","title":"这里比北京冷多了","en":"It's much colder here than in Beijing","scenes":[
  {"name":"课文1 电话聊两地天气","track":"12-1","sents":[
    ("喂，家月，是你啊！有什么事情吗？","Wèi, Jiāyuè, shì nǐ a! Yǒu shénme shìqing ma?","Hello, Jiayue, it's you! Is there anything you need?"),  # 呼语
    ("没什么事，就想跟您说说话。","Méi shénme shì, jiù xiǎng gēn nín shuōshuo huà.","Nothing in particular — I just wanted to talk to you."),
    ("好啊。你今天没课吗？","Hǎo a. Nǐ jīntiān méi kè ma?","Sure. Don't you have class today?"),
    ("下午有课。您那里天气怎么样？","Xiàwǔ yǒu kè. Nín nàlǐ tiānqì zěnmeyàng?","I have class in the afternoon. How's the weather over there?"),
    ("北京这几天虽然是晴天，但是有点儿冷。","Běijīng zhè jǐ tiān suīrán shì qíng tiān, dànshì yǒudiǎnr lěng.","Although it's been sunny in Beijing these days, it's a bit cold."),
    ("我这里比北京冷多了，外边还正下着雪呢！","Wǒ zhèlǐ bǐ Běijīng lěng duō le, wàibian hái zhèng xiàzhe xuě ne!","It's much colder here than in Beijing — it's snowing outside right now!"),
  ]},
  {"name":"课文2 叮嘱雪天少出门","track":"12-3","sents":[
    ("喂，一飞，听家月说你那边下雪了，下得大不大？","Wèi, Yīfēi, tīng Jiāyuè shuō nǐ nàbiān xià xuě le, xià de dà bu dà?","Hello, Yifei. Jiayue told me it's snowing over there. Is it heavy?"),  # 呼语
    ("今天不大，昨天比今天下得大。","Jīntiān bú dà, zuótiān bǐ jīntiān xià de dà.","Not heavy today — yesterday it snowed harder than today."),
    ("天气不好，你去外面的时候多穿点儿衣服。","Tiānqì bù hǎo, nǐ qù wàimiàn de shíhou duō chuān diǎnr yīfu.","The weather isn't good. Wear more clothes when you go outside."),
    ("这几天我在网上上课，没出去过。","Zhè jǐ tiān wǒ zài wǎngshang shàngkè, méi chūqùguo.","I've been teaching classes online these days, so I haven't gone out."),
    ("那就好，有事记得给我打电话。","Nà jiù hǎo, yǒu shì jìde gěi wǒ dǎ diànhuà.","That's good. Remember to call me if anything comes up."),
    ("好的。现在不下雪了，我出去买点儿吃的。","Hǎo de. Xiànzài bú xià xuě le, wǒ chūqù mǎi diǎnr chī de.","Okay. It's stopped snowing now, so I'll go out and buy some food."),
    ("一次多买点儿，阴天下雪什么的就少出去吧。","Yí cì duō mǎi diǎnr, yīn tiān xià xuě shénmede jiù shǎo chūqù ba.","Buy more at once, and go out less when it's cloudy or snowy."),
  ]},
  {"name":"课文3 约一起跑步","track":"12-5","sents":[
    ("喂，家月，今天天气不错，我们去跑步吧！","Wèi, Jiāyuè, jīntiān tiānqì búcuò, wǒmen qù pǎobù ba!","Hello, Jiayue! The weather is nice today — let's go for a run!"),  # 呼语
    ("你跑步跑得比我快，我们能一起跑吗？","Nǐ pǎobù pǎo de bǐ wǒ kuài, wǒmen néng yìqǐ pǎo ma?","You run faster than me. Can we really run together?"),
    ("可以的，我慢慢跑，等着你。","Kěyǐ de, wǒ mànmàn pǎo, děngzhe nǐ.","Of course. I'll run slowly and wait for you."),
    ("好吧。你真爱跑步啊！","Hǎo ba. Nǐ zhēn ài pǎobù a!","Alright. You really love running!"),
    ("我从小就经常跟爸爸跑步，跑步能让人快乐！","Wǒ cóngxiǎo jiù jīngcháng gēn bàba pǎobù, pǎobù néng ràng rén kuàilè!","I've often run with my dad since childhood. Running makes people happy!"),
    ("好，那我准备一下。","Hǎo, nà wǒ zhǔnbèi yíxià.","Okay, then I'll get ready."),
    ("我现在坐地铁去找你，一会儿楼下见。","Wǒ xiànzài zuò dìtiě qù zhǎo nǐ, yíhuìr lóu xià jiàn.","I'm taking the subway to your place now. See you downstairs in a bit."),
  ]},
  {"name":"课文4 日记·晴天跑步（叙述体）","track":"12-7","sents":[
    ("前几天天气不好，我没走路，每天坐两站地铁去学校。","Qián jǐ tiān tiānqì bù hǎo, wǒ méi zǒulù, měi tiān zuò liǎng zhàn dìtiě qù xuéxiào.","The weather was bad over the past few days, so I didn't walk — I took the subway two stops to school every day."),
    ("今天是个大晴天，李文让我跟他去外面跑步。","Jīntiān shì gè dà qíng tiān, Lǐ Wén ràng wǒ gēn tā qù wàimiàn pǎobù.","Today was a beautiful sunny day, and Li Wen asked me to go running outside with him."),
    ("他小时候经常跑步，跑得比我快，但是他会等我。","Tā xiǎoshíhou jīngcháng pǎobù, pǎo de bǐ wǒ kuài, dànshì tā huì děng wǒ.","He ran often as a child and runs faster than me, but he waits for me."),
    ("跟李文一起跑步，我好高兴啊！","Gēn Lǐ Wén yìqǐ pǎobù, wǒ hǎo gāoxìng a!","Running with Li Wen made me so happy!"),
  ]},
]},
{"id":"lesson-13","title":"我们爱上中文课","en":"We love attending Chinese class","scenes":[
  {"name":"课文1 教室聊新年送礼","track":"13-1","sents":[
    ("时间过得真快啊！新年就要到了。","shí jiān guò de zhēn kuài a xīn nián jiù yào dào le","Time flies! The New Year is almost here."),
    ("这一年王老师教我们中文，每天工作都很累。","zhè yì nián wáng lǎo shī jiāo wǒ men zhōng wén měi tiān gōng zuò dōu hěn lèi","This year Ms. Wang has been teaching us Chinese, and she works so hard every day."),
    ("是啊，她教得很好。因为她，我们都非常爱上中文课。","shì a tā jiāo de hěn hǎo yīn wèi tā wǒ men dōu fēi cháng ài shàng zhōng wén kè","Yes, she teaches very well. Because of her, we all love attending Chinese class."),
    ("我们给她准备个新年礼物吧。你觉得送给她什么好呢？","wǒ men gěi tā zhǔn bèi gè xīn nián lǐ wù ba nǐ jué de sòng gěi tā shén me hǎo ne","Let's prepare a New Year's gift for her. What do you think we can present to her?"),
    ("王老师喜欢花，就送给她花吧。","wáng lǎo shī xǐ huan huā jiù sòng gěi tā huā ba","Ms. Wang likes flowers. I think we can give her flowers."),
    ("那我们去花店看看，现在买花的人多，希望花店还有漂亮的花。","nà wǒ men qù huā diàn kàn kan xiàn zài mǎi huā de rén duō xī wàng huā diàn hái yǒu piào liang de huā","Then let's go to the flower shop; there are many people buying flowers now. I hope there are still some beautiful flowers in the shop."),
  ]},  # 气泡数核对：6
  {"name":"课文2 课堂听写辨字","track":"13-3","sents":[
    ("王老师，今天的词比昨天多了十个。","wáng lǎo shī jīn tiān de cí bǐ zuó tiān duō le shí gè","Ms. Wang, today's vocabulary has ten more words than yesterday's."),
    ("是啊！你们都学会了吗？","shì a nǐ men dōu xué huì le ma","Yes! Have you all learned them?"),
    ("学会了，没有问题。","xué huì le méi yǒu wèn tí","We've learned them. No problem."),
    ("好。现在我来说，你们在本子上面写。","hǎo xiàn zài wǒ lái shuō nǐ men zài běn zi shàng miàn xiě","Good. Now I'll say them, and you write them down in your notebooks."),
    # ⚠️ 教材此处印有「……」（p129 第4、5个气泡之间，页面左侧独立一行，英译栏同位置也印 "..."）——听写课堂过程省略，音轨此处可能有额外语音段
    ("同学们，“洗手间”的“间”字写错了，它的里面是“日”，不是“口”。","tóng xué men xǐ shǒu jiān de jiān zì xiě cuò le tā de lǐ miàn shì rì bú shì kǒu","Class, the character 间 in 洗手间 is wrong. The part inside is 日, not 口."),
    ("“日”比“口”多一笔，写“口”就是“问题”的“问”了。","rì bǐ kǒu duō yì bǐ xiě kǒu jiù shì wèn tí de wèn le","日 has one more stroke than 口. Writing 口 turns it into the 问 in 问题."),
    ("没错，你说得很对。","méi cuò nǐ shuō de hěn duì","Yes, you are right."),
  ]},  # 气泡数核对：7
  {"name":"课文3 夸本子谈回礼","track":"13-5","sents":[
    ("家月，你觉得这个本子怎么样？","jiā yuè nǐ jué de zhè ge běn zi zěn me yàng","Jiayue, what do you think of this notebook?"),
    ("很漂亮，多少钱一个？","hěn piào liang duō shao qián yí gè","It's very pretty. How much is it?"),
    ("比我们一起买的那个本子贵一点儿。","bǐ wǒ men yì qǐ mǎi de nà ge běn zi guì yì diǎnr","It's a bit more expensive than the notebook we bought together."),
    ("这么漂亮的本子，不可能贵一点儿吧？","zhè me piào liang de běn zi bù kě néng guì yì diǎnr ba","For such a beautiful notebook, it couldn't be just a little more expensive, right?"),
    ("我是上网买的，真没那么贵。我买了两个，送你一个。","wǒ shì shàng wǎng mǎi de zhēn méi nà me guì wǒ mǎi le liǎng gè sòng nǐ yí gè","I bought it online, and it's really not that expensive. I bought two and will give you one."),
    ("谢谢！那我送给你什么呢？","xiè xie nà wǒ sòng gěi nǐ shén me ne","Thank you! Then what should I give you in return?"),
    ("咖啡杯吧，我最喜欢喝咖啡了。","kā fēi bēi ba wǒ zuì xǐ huan hē kā fēi le","A coffee cup would be great. I like drinking coffee the most."),
    ("好，那样我们就都有新年礼物了！","hǎo nà yàng wǒ men jiù dōu yǒu xīn nián lǐ wù le","Alright! Then we'll both have New Year's gifts!"),
  ]},  # 气泡数核对：8
  {"name":"课文4 日记记新年礼物（叙述体）","track":"13-7","sents":[
    ("新年就要到了，安妮送给我一个新本子。","xīn nián jiù yào dào le ān nī sòng gěi wǒ yí gè xīn běn zi","The New Year is almost here. Annie gave me a new notebook."),
    ("她告诉我是在网上买的，比我的本子贵一点儿。","tā gào su wǒ shì zài wǎng shang mǎi de bǐ wǒ de běn zi guì yì diǎnr","She told me she bought it online, and it's a bit more expensive than mine."),
    ("我们班同学也送了王老师漂亮的花，希望她高高兴兴地过个新年。","wǒ men bān tóng xué yě sòng le wáng lǎo shī piào liang de huā xī wàng tā gāo gāo xìng xìng de guò gè xīn nián","Our classmates also gave Ms. Wang beautiful flowers, hoping she will have a happy New Year."),
  ]},  # 叙述体逐句拆分；句数核对：3
]},
{"id":"lesson-14","title":"一个人过年多没意思啊","en":"It's boring to celebrate the Spring Festival alone","scenes":[
  {"name":"课文1 楼下站着一个人","track":"14-1","sents":[
    ("王老师，你家楼下站着一个人。","wáng lǎo shī nǐ jiā lóu xià zhàn zhe yí gè rén","Ms. Wang, there's someone standing downstairs at your building."),
    ("我家楼下？我看看。","wǒ jiā lóu xià wǒ kàn kan","Downstairs at my building? Let me take a look."),
    ("那个人穿着黑色的裤子，手里还拿着一个黑色的包。","nà ge rén chuān zhe hēi sè de kù zi shǒu li hái ná zhe yí gè hēi sè de bāo","That person is wearing black pants and holding a black bag."),
    ("我看见那个人了，他是我男朋友。","wǒ kàn jiàn nà ge rén le tā shì wǒ nán péng you","I see him. He is my boyfriend."),
    ("那我们快过去吧。","nà wǒ men kuài guò qù ba","Let's go over quickly then."),
  ]},  # 气泡数核对：5
  {"name":"课文2 楼下重逢与介绍","track":"14-3","sents":[
    ("同乐，真是你啊！上次打电话，你说有时间过来看我，没想到这么快就来了！","tóng lè zhēn shì nǐ a shàng cì dǎ diàn huà nǐ shuō yǒu shí jiān guò lái kàn wǒ méi xiǎng dào zhè me kuài jiù lái le","Tongle, it really is you! Last time we talked on the phone, you said you'd visit me when you had time. I didn't expect you to come so soon!"),
    ("就要过年了，你一个人在这儿多没意思啊，所以我就早早过来了。","jiù yào guò nián le nǐ yí gè rén zài zhèr duō méi yì si a suǒ yǐ wǒ jiù zǎo zǎo guò lái le","The Spring Festival is almost here. It's no fun for you to be here all alone, so I came here as soon as possible."),
    ("你能来，我太高兴了！","nǐ néng lái wǒ tài gāo xìng le","I'm so happy you could come!"),
    ("一飞，你旁边这位是？","yī fēi nǐ páng biān zhè wèi shì","Yifei, who's this next to you?"),
    ("同乐，这是李文，他在我们学校学医。李文，这是我男朋友杨同乐。","tóng lè zhè shì lǐ wén tā zài wǒ men xué xiào xué yī lǐ wén zhè shì wǒ nán péng you yáng tóng lè","Tongle, this is Li Wen. He's studying medicine at our school. Li Wen, this is my boyfriend, Yang Tongle."),
    ("李文，很高兴认识你！","lǐ wén hěn gāo xìng rèn shi nǐ","Li Wen, nice to meet you!"),
    ("认识你我也很高兴！我家就在前面那个楼，有时间来玩。","rèn shi nǐ wǒ yě hěn gāo xìng wǒ jiā jiù zài qián miàn nà ge lóu yǒu shí jiān lái wán","Nice to meet you too! My home is just in that building up ahead. Feel free to come over when you have time."),
  ]},  # 气泡数核对：7
  {"name":"课文3 客厅聊房子邻居","track":"14-5","sents":[
    ("一飞，你住的房子真不错，很大，离学校也不远。","yī fēi nǐ zhù de fáng zi zhēn bú cuò hěn dà lí xué xiào yě bù yuǎn","Yifei, your house is really nice, very big, and not far from school."),
    ("是啊！我楼下还住着一家中国人，他们人很好。","shì a wǒ lóu xià hái zhù zhe yì jiā zhōng guó rén tā men rén hěn hǎo","Yes! There's a Chinese family living downstairs, and they are very nice."),
    ("这样你有事情就可以找他们帮忙。","zhè yàng nǐ yǒu shì qing jiù kě yǐ zhǎo tā men bāng máng","Then you can ask them for help if you ever need anything."),
    ("对，我也帮他们家的小孩儿学中文。","duì wǒ yě bāng tā men jiā de xiǎo háir xué zhōng wén","Yes, I also help their child learn Chinese."),
    ("我记得你跟我说过，是个女孩儿，学得也很好。","wǒ jì de nǐ gēn wǒ shuō guo shì gè nǚ háir xué de yě hěn hǎo","I remember you told me that child was a girl, and she learned so well."),
    ("没错，她经常跑上来找我玩。","méi cuò tā jīng cháng pǎo shàng lái zhǎo wǒ wán","Exactly, she often comes upstairs to play with me."),
    ("你问问他们什么时候有时间，我请他们吃个饭。","nǐ wèn wen tā men shén me shí hou yǒu shí jiān wǒ qǐng tā men chī gè fàn","You can ask them when they're free, and I'll treat them to a meal."),
  ]},  # 气泡数核对：7
  {"name":"课文4 日记写男朋友（叙述体）","track":"14-7","sents":[
    ("我男朋友姓杨，叫杨同乐。","wǒ nán péng you xìng yáng jiào yáng tóng lè","My boyfriend's last name is Yang, and his full name is Yang Tongle."),
    ("他高个子、大眼睛，唱歌唱得很好，跳舞跳得也不错。","tā gāo gè zi dà yǎn jing chàng gē chàng de hěn hǎo tiào wǔ tiào de yě bú cuò","He is tall, has big eyes, sings very well, and is also good at dancing."),
    # ⚠️ 教材 p142 英译把「姐姐」译成 cousin，与汉语不符；此处按汉语原文译 older sister（子代理看图核出）
    ("他和我姐姐一起工作，是姐姐介绍我们认识的。","tā hé wǒ jiě jie yì qǐ gōng zuò shì jiě jie jiè shào wǒ men rèn shi de","He works with my older sister, and it was she who introduced us."),
    ("他告诉我，从见到我的第一天开始，他就喜欢上我了。","tā gào su wǒ cóng jiàn dào wǒ de dì yī tiān kāi shǐ tā jiù xǐ huan shàng wǒ le","He told me that he liked me from the very first day he met me."),
  ]},  # 叙述体逐句拆分；句数核对：4
]},
{"id":"lesson-15","title":"我想再去一次中国","en":"I want to go to China again","scenes":[
  {"name":"课文1 考场谈考后打算","track":"15-1","sents":[
    ("考试就要开始了，请大家写上姓名，写好后就可以做题了。","kǎo shì jiù yào kāi shǐ le qǐng dà jiā xiě shàng xìng míng xiě hǎo hòu jiù kě yǐ zuò tí le","The exam is about to begin. Please write down your name, and once you're done, you can start answering the questions."),
    # ⚠️ 教材此处印有「……」（p145 第1、2个气泡之间）——考试过程省略，音轨此处可能有额外语音段
    ("老师，我做完了。","lǎo shī wǒ zuò wán le","Teacher, I'm finished."),
    ("老师，我也做完了。","lǎo shī wǒ yě zuò wán le","Teacher, I'm finished too."),
    ("……对了，你们考完试想做什么？","duì le nǐ men kǎo wán shì xiǎng zuò shén me","... Oh, what are you going to do after the exam?"),
    ("我很想去中国，虽然去过一次，但是很想再去一次。","wǒ hěn xiǎng qù zhōng guó suī rán qù guo yí cì dàn shì hěn xiǎng zài qù yí cì","I want to go to China. I've been there once, but I really want to go again."),
    ("不错，到中国后你就可以经常说中文了。","bú cuò dào zhōng guó hòu nǐ jiù kě yǐ jīng cháng shuō zhōng wén le","Good, you can often speak Chinese in China."),
  ]},  # 气泡数核对：6
  {"name":"课文2 咖啡店聊北京行","track":"15-3","sents":[
    ("考完试了，我现在可以出国旅游了。","kǎo wán shì le wǒ xiàn zài kě yǐ chū guó lǚ yóu le","The exam is over, so now I can travel abroad."),
    ("你要去哪儿？","nǐ yào qù nǎr","Where are you planning to go?"),
    ("我要再去一次北京。","wǒ yào zài qù yí cì běi jīng","I want to go to Beijing again."),
    ("为什么还去北京？","wèi shén me hái qù běi jīng","Why Beijing again?"),
    ("因为我想再吃一次烤鸭，再喝一次奶茶，再去北京大学看一次电影……","yīn wèi wǒ xiǎng zài chī yí cì kǎo yā zài hē yí cì nǎi chá zài qù běi jīng dà xué kàn yí cì diàn yǐng","Because I want to eat Peking Duck again, drink bubble tea again, and watch a movie at Peking University again..."),
    ("你想做的事情很多啊！","nǐ xiǎng zuò de shì qing hěn duō a","You want to do a lot of things!"),
    ("是啊，你看，我还在网上买好颐和园的门票了呢。","shì a nǐ kàn wǒ hái zài wǎng shang mǎi hǎo yí hé yuán de mén piào le ne","Yes, look, I've already bought a ticket for the Summer Palace online."),
    ("我的高中同学就在颐和园上班，可以让他给你好好介绍介绍。","wǒ de gāo zhōng tóng xué jiù zài yí hé yuán shàng bān kě yǐ ràng tā gěi nǐ hǎo hǎo jiè shào jiè shào","One of my high school classmates works at the Summer Palace, and he can give you a great tour."),
    ("太好了！出门旅游，多个朋友多条路。","tài hǎo le chū mén lǚ yóu duō gè péng you duō tiáo lù","That's amazing! When you travel, the more friends you have, the more paths you have."),
  ]},  # 气泡数核对：9
  {"name":"课文3 聊回国和机票","track":"15-5","sents":[
    ("李文，你有一年没回国了吧？","lǐ wén nǐ yǒu yì nián méi huí guó le ba","Li Wen, you haven't been back to China for a year, right?"),
    ("不到一年。我六月的时候回去了一次。","bú dào yì nián wǒ liù yuè de shí hou huí qù le yí cì","Not quite a year. I went back once this June."),
    ("我怎么忘了？还是我送你去的机场呢。","wǒ zěn me wàng le hái shì wǒ sòng nǐ qù de jī chǎng ne","How could I forget? I was the one who took you to the airport."),
    ("是啊。","shì a","Yes."),
    ("我记得你那次的机票很便宜。","wǒ jì de nǐ nà cì de jī piào hěn pián yi","I remember your air ticket was very cheap."),
    ("没错，可能因为那个时候去北京的人不多吧。","méi cuò kě néng yīn wèi nà ge shí hou qù běi jīng de rén bù duō ba","Exactly. Maybe it was because there weren't many people going to Beijing at that time."),
    ("这次的机票虽然有点儿贵，但想到就要飞北京了，我还是很高兴的。","zhè cì de jī piào suī rán yǒu diǎnr guì dàn xiǎng dào jiù yào fēi běi jīng le wǒ hái shì hěn gāo xìng de","The air ticket is a little expensive this time, but I am so happy thinking about going to Beijing."),
  ]},  # 气泡数核对：7
  {"name":"课文4 日记盼回家过年（叙述体）","track":"15-7","sents":[
    ("我六月的时候回过一次北京，现在有半年多没回去了，我有点儿想家。","wǒ liù yuè de shí hou huí guo yí cì běi jīng xiàn zài yǒu bàn nián duō méi huí qù le wǒ yǒu diǎnr xiǎng jiā","I went back to Beijing once this June, and now it has been over six months since I last went back. I miss home a bit."),
    ("就要过年了，我要回家过年。","jiù yào guò nián le wǒ yào huí jiā guò nián","The Spring Festival is coming, and I'll be going back to celebrate it."),
    ("家月这次也要去北京，我们都是星期五的飞机。","jiā yuè zhè cì yě yào qù běi jīng wǒ men dōu shì xīng qī wǔ de fēi jī","Jiayue is also going to Beijing—we're both on the same flight this Friday."),
    ("家月说我们好像小鸟，一起飞到北京，再一起飞回这里。","jiā yuè shuō wǒ men hǎo xiàng xiǎo niǎo yì qǐ fēi dào běi jīng zài yì qǐ fēi huí zhè lǐ","Jiayue said we are like little birds, flying to Beijing together and then flying back here together."),
  ]},  # 叙述体逐句拆分；句数核对：4
]},
]

# 拼音串清洗: 各课转录时标点风格不一(有的带逗号/句号/连字符),统一去掉——
# compile_lib.compile_sentence 按字符流逐字消费拼音,混入标点会导致音节错位
import re as _re
_PUNC = _re.compile(r"[,\.\?!;:\-\u2013\u2014\u2026\u201c\u201d\u2018\u2019\"\u3001\u3002\uff0c\uff1f\uff01\uff1a\uff1b]")
for _L in LESSONS:
    for _sc in _L["scenes"]:
        _sc["sents"] = [(s[0], _PUNC.sub(" ", s[1]), *s[2:]) for s in _sc["sents"]]
