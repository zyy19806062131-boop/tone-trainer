# HSK标准教程1 课文原文 —— 逐句转录（来源:《HSK标准教程1》PDF 各课"课文"部分）
# 每课: id, 标题(教材真实课名), en标题, scenes[ {name, sents:[(zh, py_textbook, en)] } ]
# py_textbook = 教材给出的带声调拼音(含变调/轻声),音节空格分隔;数字一律用汉字以对齐声调格
# 数字用汉字: 三/四/五十/二十 等(教材口语读法),便于逐字声调格对齐

LESSONS = [
  # L1 (语音课·打招呼)
  {"id":"lesson-01","title":"你好","en":"Hello","scenes":[
    {"name":"打招呼 Greeting","track":"01-1","sents":[
      ("你好！","Nǐ hǎo","Hello!"),
      ("你好！","Nǐ hǎo","Hello!"),
    ]},
    {"name":"打招呼 Greeting","track":"01-2","sents":[
      ("您好！","Nín hǎo","Hello!"),
      ("你们好！","Nǐmen hǎo","Hello!"),
    ]},
    {"name":"道歉 Apologizing","track":"01-3","sents":[
      ("对不起！","Duìbuqǐ","I'm sorry!"),
      ("没关系！","Méi guānxi","That's OK!"),
    ]},
  ]},
  # L2 (语音课·致谢告别)
  {"id":"lesson-02","title":"谢谢你","en":"Thank you","scenes":[
    {"name":"致谢 Thanking","track":"02-1","sents":[
      ("谢谢！","Xièxie","Thank you!"),
      ("不谢！","Bú xiè","Sure!"),
    ]},
    {"name":"致谢 Thanking","track":"02-2","sents":[
      ("谢谢你！","Xièxie nǐ","Thank you!"),
      ("不客气！","Bú kèqi","You're welcome!"),
    ]},
    {"name":"告别 Saying goodbye","track":"02-3","sents":[
      ("再见！","Zàijiàn","Goodbye!"),
      ("再见！","Zàijiàn","Bye!"),
    ]},
  ]},
  # L3
  {"id":"lesson-03","title":"你叫什么名字","en":"What's your name","scenes":[
    {"name":"在学校 In the school","track":"03-1","sents":[
      ("你叫什么名字？","Nǐ jiào shénme míngzi","What's your name?"),
      ("我叫李月。","Wǒ jiào Lǐ Yuè","My name is Li Yue."),
    ]},
    {"name":"在教室 In the classroom","track":"03-2","sents":[
      ("你是老师吗？","Nǐ shì lǎoshī ma","Are you a teacher?"),
      ("我不是老师，我是学生。","Wǒ bú shì lǎoshī wǒ shì xuésheng","No, I'm not. I'm a student."),
    ]},
    {"name":"在学校 In the school","track":"03-3","sents":[
      ("你是中国人吗？","Nǐ shì Zhōngguó rén ma","Are you Chinese?"),
      ("我不是中国人，我是美国人。","Wǒ bú shì Zhōngguó rén wǒ shì Měiguó rén","No, I'm not. I'm American."),
    ]},
  ]},
  # L4
  {"id":"lesson-04","title":"她是我的汉语老师","en":"She is my Chinese teacher","scenes":[
    {"name":"在教室 In the classroom","track":"04-1","sents":[
      ("她是谁？","Tā shì shéi","Who is she?"),
      ("她是我的汉语老师，她叫李月。","Tā shì wǒ de Hànyǔ lǎoshī tā jiào Lǐ Yuè","She is my Chinese teacher. Her name is Li Yue."),
    ]},
    {"name":"在图书馆 In the library","track":"04-2","sents":[
      ("你是哪国人？","Nǐ shì nǎ guó rén","Which country are you from?"),
      ("我是美国人。你呢？","Wǒ shì Měiguó rén nǐ ne","I'm American. What about you?"),
      ("我是中国人。","Wǒ shì Zhōngguó rén","I'm Chinese."),
    ]},
    {"name":"看照片 Looking at the photo","track":"04-3","sents":[
      ("他是谁？","Tā shì shéi","Who is he?"),
      ("他是我同学。","Tā shì wǒ tóngxué","He is my classmate."),
      ("她呢？她是你同学吗？","Tā ne tā shì nǐ tóngxué ma","What about her? Is she your classmate?"),
      ("她不是我同学，她是我朋友。","Tā bú shì wǒ tóngxué tā shì wǒ péngyou","No, she isn't. She is my friend."),
    ]},
  ]},
  # L5
  {"id":"lesson-05","title":"她女儿今年二十岁","en":"Her daughter is 20 years old this year","scenes":[
    {"name":"在学校 In the school","track":"05-1","sents":[
      ("你家有几口人？","Nǐ jiā yǒu jǐ kǒu rén","How many people are there in your family?"),
      ("我家有三口人。","Wǒ jiā yǒu sān kǒu rén","There are three."),
    ]},
    {"name":"在办公室 In the office","track":"05-2","sents":[
      ("你女儿几岁了？","Nǐ nǚ'ér jǐ suì le","How old is your daughter?"),
      ("她今年四岁了。","Tā jīnnián sì suì le","She is four years old."),
    ]},
    {"name":"在办公室 In the office","track":"05-3","sents":[
      ("李老师多大了？","Lǐ lǎoshī duō dà le","How old is Professor Li?"),
      ("她今年五十岁了。","Tā jīnnián wǔshí suì le","She is 50 years old."),
      ("她女儿呢？","Tā nǚ'ér ne","What about her daughter?"),
      ("她女儿今年二十岁。","Tā nǚ'ér jīnnián èrshí suì","Her daughter is 20."),
    ]},
  ]},
  # L6
  {"id":"lesson-06","title":"我会说汉语","en":"I can speak Chinese","scenes":[
    {"name":"在学校 In the school","track":"06-1","sents":[
      ("你会说汉语吗？","Nǐ huì shuō Hànyǔ ma","Can you speak Chinese?"),
      ("我会说汉语。","Wǒ huì shuō Hànyǔ","Yes, I can."),
      ("你妈妈会说汉语吗？","Nǐ māma huì shuō Hànyǔ ma","Can your mother speak Chinese?"),
      ("她不会说。","Tā bú huì shuō","No, she can't."),
    ]},
    {"name":"在厨房 In the kitchen","track":"06-2","sents":[
      ("中国菜好吃吗？","Zhōngguó cài hǎo chī ma","Is Chinese food delicious?"),
      ("中国菜很好吃。","Zhōngguó cài hěn hǎochī","Yes, quite delicious."),
      ("你会做中国菜吗？","Nǐ huì zuò Zhōngguó cài ma","Can you cook Chinese food?"),
      ("我不会做。","Wǒ bú huì zuò","No, I can't."),
    ]},
    {"name":"在图书馆 In the library","track":"06-3","sents":[
      ("你会写汉字吗？","Nǐ huì xiě Hànzì ma","Can you write Chinese characters?"),
      ("我会写。","Wǒ huì xiě","Yes, I can."),
      ("这个字怎么写？","Zhège zì zěnme xiě","How do you write this character?"),
      ("对不起，这个字我会读，不会写。","Duìbuqǐ zhège zì wǒ huì dú bú huì xiě","Sorry. I can read it, but I don't know how to write it."),
    ]},
  ]},
  # L7
  {"id":"lesson-07","title":"今天几号","en":"What's the date today","scenes":[
    {"name":"在银行 In a bank","track":"07-1","sents":[
      ("请问，今天几号？","Qǐngwèn jīntiān jǐ hào","Excuse me, what's the date today?"),
      ("今天九月一号。","Jīntiān jiǔ yuè yī hào","It's September 1st."),
      ("今天星期几？","Jīntiān xīngqī jǐ","What day is it today?"),
      ("星期三。","Xīngqī sān","It's Wednesday."),
    ]},
    {"name":"看日历 Look at the calendar","track":"07-2","sents":[
      ("昨天是几月几号？","Zuótiān shì jǐ yuè jǐ hào","What was the date yesterday?"),
      ("昨天是八月三十一号，星期二。","Zuótiān shì bā yuè sānshíyī hào xīngqī èr","It was Tuesday, August 31st."),
      ("明天呢？","Míngtiān ne","What about tomorrow?"),
      ("明天是九月二号，星期四。","Míngtiān shì jiǔ yuè èr hào xīngqī sì","It's Thursday, September 2nd."),
    ]},
    {"name":"在咖啡馆儿 In a coffee house","track":"07-3","sents":[
      ("明天星期六，你去学校吗？","Míngtiān xīngqī liù nǐ qù xuéxiào ma","Tomorrow is Saturday. Will you go to school?"),
      ("我去学校。","Wǒ qù xuéxiào","Yes, I will."),
      ("你去学校做什么？","Nǐ qù xuéxiào zuò shénme","What are you going to do there?"),
      ("我去学校看书。","Wǒ qù xuéxiào kàn shū","I'm going there to do some reading."),
    ]},
  ]},
  # L8
  {"id":"lesson-08","title":"我想喝茶","en":"I'd like some tea","scenes":[
    {"name":"在饭馆儿 In a restaurant","track":"08-1","sents":[
      ("你想喝什么？","Nǐ xiǎng hē shénme","What would you like to drink?"),
      ("我想喝茶。","Wǒ xiǎng hē chá","I'd like some tea."),
      ("你想吃什么？","Nǐ xiǎng chī shénme","What would you like to eat?"),
      ("我想吃米饭。","Wǒ xiǎng chī mǐfàn","I'd like rice."),
    ]},
    {"name":"在客厅 In the living room","track":"08-2","sents":[
      ("下午你想做什么？","Xiàwǔ nǐ xiǎng zuò shénme","What would you like to do this afternoon?"),
      ("下午我想去商店。","Xiàwǔ wǒ xiǎng qù shāngdiàn","I'd like to go shopping."),
      ("你想买什么？","Nǐ xiǎng mǎi shénme","What do you want to buy?"),
      ("我想买一个杯子。","Wǒ xiǎng mǎi yí ge bēizi","I want to buy a cup."),
    ]},
    {"name":"在商店 In a store","track":"08-3","sents":[
      ("你好！这个杯子多少钱？","Nǐ hǎo zhège bēizi duōshao qián","Hello! How much is this cup?"),
      ("二十八块。","Èrshíbā kuài","28 yuan."),
      ("那个杯子多少钱？","Nàge bēizi duōshao qián","What about that one?"),
      ("那个杯子十八块钱。","Nàge bēizi shíbā kuài qián","That one is 18 yuan."),
    ]},
  ]},
  # L9
  {"id":"lesson-09","title":"你儿子在哪儿工作","en":"Where does your son work","scenes":[
    {"name":"在家 At home","track":"09-1","sents":[
      ("小猫在哪儿？","Xiǎo māo zài nǎr","Where is the kitty?"),
      ("小猫在那儿。","Xiǎo māo zài nàr","The kitty is over there."),
      ("小狗在哪儿？","Xiǎo gǒu zài nǎr","Where is the puppy?"),
      ("小狗在椅子下面。","Xiǎo gǒu zài yǐzi xiàmiàn","The puppy is under the chair."),
    ]},
    {"name":"在车站 At the railway station","track":"09-2","sents":[
      ("你在哪儿工作？","Nǐ zài nǎr gōngzuò","Where do you work?"),
      ("我在学校工作。","Wǒ zài xuéxiào gōngzuò","I work in a school."),
      ("你儿子在哪儿工作？","Nǐ érzi zài nǎr gōngzuò","Where does your son work?"),
      ("我儿子在医院工作，他是医生。","Wǒ érzi zài yīyuàn gōngzuò tā shì yīshēng","My son works in a hospital. He is a doctor."),
    ]},
    {"name":"打电话 On the phone","track":"09-3","sents":[
      ("你爸爸在家吗？","Nǐ bàba zài jiā ma","Is your father at home?"),
      ("不在家。","Bú zài jiā","No, he isn't."),
      ("他在哪儿呢？","Tā zài nǎr ne","Where is he?"),
      ("他在医院。","Tā zài yīyuàn","He is in the hospital."),
    ]},
  ]},
  # L10
  {"id":"lesson-10","title":"我能坐这儿吗","en":"Can I sit here","scenes":[
    {"name":"在办公室 In the office","track":"10-1","sents":[
      ("桌子上有什么？","Zhuōzi shang yǒu shénme","What are there on the desk?"),
      ("桌子上有一个电脑和一本书。","Zhuōzi shang yǒu yí ge diànnǎo hé yì běn shū","There is a computer and a book."),
      ("杯子在哪儿？","Bēizi zài nǎr","Where is the cup?"),
      ("杯子在桌子里。","Bēizi zài zhuōzi li","It's in the desk."),
    ]},
    {"name":"在健身房 In the gym","track":"10-2","sents":[
      ("前面那个人叫什么名字？","Qiánmiàn nàge rén jiào shénme míngzi","Who is the person in the front?"),
      ("她叫王方，在医院工作。","Tā jiào Wáng Fāng zài yīyuàn gōngzuò","She is Wang Fang. She works in a hospital."),
      ("后面那个人呢？他叫什么名字？","Hòumiàn nàge rén ne tā jiào shénme míngzi","What about the person at the back? What's his name?"),
      ("他叫谢朋，在商店工作。","Tā jiào Xiè Péng zài shāngdiàn gōngzuò","He is Xie Peng. He works in a store."),
    ]},
    {"name":"在图书馆 In the library","track":"10-3","sents":[
      ("这儿有人吗？","Zhèr yǒu rén ma","Is this seat taken?"),
      ("没有。","Méi yǒu","No, it isn't."),
      ("我能坐这儿吗？","Wǒ néng zuò zhèr ma","Can I sit here?"),
      ("请坐。","Qǐng zuò","Yes, please."),
    ]},
  ]},
  # L11
  {"id":"lesson-11","title":"现在几点","en":"What's the time now","scenes":[
    {"name":"在图书馆 In the library","track":"11-1","sents":[
      ("现在几点？","Xiànzài jǐ diǎn","What's the time now?"),
      ("现在十点十分。","Xiànzài shí diǎn shí fēn","It's ten past ten."),
      ("中午几点吃饭？","Zhōngwǔ jǐ diǎn chī fàn","When shall we have our lunch?"),
      ("十二点吃饭。","Shí'èr diǎn chī fàn","At twelve o'clock."),
    ]},
    {"name":"在家 At home","track":"11-2","sents":[
      ("爸爸什么时候回家？","Bàba shénme shíhou huí jiā","When is father coming home?"),
      ("下午五点。","Xiàwǔ wǔ diǎn","At five o'clock in the afternoon."),
      ("我们什么时候去看电影？","Wǒmen shénme shíhou qù kàn diànyǐng","When are we going to see the movie?"),
      ("六点三十分。","Liù diǎn sānshí fēn","At half past six."),
    ]},
    {"name":"在家 At home","track":"11-3","sents":[
      ("我星期一去北京。","Wǒ xīngqī yī qù Běijīng","I'll go to Beijing next Monday."),
      ("你想在北京住几天？","Nǐ xiǎng zài Běijīng zhù jǐ tiān","How long will you stay in Beijing?"),
      ("住三天。","Zhù sān tiān","For three days."),
      ("星期五前能回家吗？","Xīngqī wǔ qián néng huí jiā ma","Can you come back before Friday?"),
      ("能。","Néng","Yes, I can."),
    ]},
  ]},
  # L12
  {"id":"lesson-12","title":"明天天气怎么样","en":"What will the weather be like tomorrow","scenes":[
    {"name":"在路上 On the road","track":"12-1","sents":[
      ("昨天北京的天气怎么样？","Zuótiān Běijīng de tiānqì zěnmeyàng","How was the weather in Beijing yesterday?"),
      ("太热了。","Tài rè le","It was too hot."),
      ("明天呢？明天天气怎么样？","Míngtiān ne míngtiān tiānqì zěnmeyàng","What about tomorrow? What will the weather be like tomorrow?"),
      ("明天天气很好，不冷不热。","Míngtiān tiānqì hěn hǎo bù lěng bú rè","It will be fine, neither cold nor hot."),
    ]},
    {"name":"在健身房 In the gym","track":"12-2","sents":[
      ("今天会下雨吗？","Jīntiān huì xià yǔ ma","Will it rain today?"),
      ("今天不会下雨。","Jīntiān bú huì xià yǔ","No, it won't rain."),
      ("王小姐今天会来吗？","Wáng xiǎojiě jīntiān huì lái ma","Will Miss Wang come today?"),
      ("不会来，天气太冷了。","Bú huì lái tiānqì tài lěng le","No, she won't. It's too cold."),
    ]},
    {"name":"在病房 In the sickroom","track":"12-3","sents":[
      ("你身体怎么样？","Nǐ shēntǐ zěnmeyàng","How are you?"),
      ("我身体不太好。天气太热了，不爱吃饭。","Wǒ shēntǐ bú tài hǎo tiānqì tài rè le bú ài chī fàn","Not very well. It's too hot. I have no appetite."),
      ("你多吃些水果，多喝水。","Nǐ duō chī xiē shuǐguǒ duō hē shuǐ","Eat more fruit and drink more water."),
      ("谢谢你，医生。","Xièxie nǐ yīshēng","Thank you, doctor."),
    ]},
  ]},
  # L13
  {"id":"lesson-13","title":"他在学做中国菜呢","en":"He is learning to cook Chinese food","scenes":[
    {"name":"打电话 On the phone","track":"13-1","sents":[
      ("喂，你在做什么呢？","Wèi nǐ zài zuò shénme ne","Hello, what are you doing?"),
      ("我在看书呢。","Wǒ zài kàn shū ne","I'm reading."),
      ("大卫也在看书吗？","Dàwèi yě zài kàn shū ma","Is David reading too?"),
      ("他没看书，他在学做中国菜呢。","Tā méi kàn shū tā zài xué zuò Zhōngguó cài ne","No, he isn't. He is learning to cook Chinese food."),
    ]},
    {"name":"在咖啡馆儿 In a coffee house","track":"13-2","sents":[
      ("昨天上午你在做什么呢？","Zuótiān shàngwǔ nǐ zài zuò shénme ne","What were you doing yesterday morning?"),
      ("我在睡觉呢。你呢？","Wǒ zài shuì jiào ne nǐ ne","I was sleeping. What about you?"),
      ("我在家看电视呢。你喜欢看电视吗？","Wǒ zài jiā kàn diànshì ne nǐ xǐhuan kàn diànshì ma","I was watching TV at home. Do you like watching TV?"),
      ("我不喜欢看电视，我喜欢看电影。","Wǒ bù xǐhuan kàn diànshì wǒ xǐhuan kàn diànyǐng","No, I don't. I like seeing movies."),
    ]},
    {"name":"在学校办公室 In the school office","track":"13-3","sents":[
      ("八二三零四一五五，这是李老师的电话吗？","Bā èr sān líng sì yāo wǔ wǔ zhè shì Lǐ lǎoshī de diànhuà ma","82304155. Is that Ms. Li's telephone number?"),
      ("不是。她的电话是八二三零四一五六。","Bú shì tā de diànhuà shì bā èr sān líng sì yāo wǔ liù","No. Her number is 82304156."),
      ("好，我现在给她打电话。","Hǎo wǒ xiànzài gěi tā dǎ diànhuà","OK. I'll call her right now."),
      ("她在工作呢，你下午打吧。","Tā zài gōngzuò ne nǐ xiàwǔ dǎ ba","She is working. Call her in the afternoon."),
    ]},
  ]},
  # L14
  {"id":"lesson-14","title":"她买了不少衣服","en":"She has bought quite a few clothes","scenes":[
    {"name":"在宿舍 In the dorm","track":"14-1","sents":[
      ("昨天上午你去哪儿了？","Zuótiān shàngwǔ nǐ qù nǎr le","Where did you go yesterday morning?"),
      ("我去商店买东西了。","Wǒ qù shāngdiàn mǎi dōngxi le","I went shopping."),
      ("你买什么了？","Nǐ mǎi shénme le","What did you buy?"),
      ("我买了一点儿苹果。","Wǒ mǎile yìdiǎnr píngguǒ","I bought some apples."),
    ]},
    {"name":"在公司 In the company","track":"14-2","sents":[
      ("你看见张先生了吗？","Nǐ kànjiàn Zhāng xiānsheng le ma","Have you seen Mr. Zhang?"),
      ("看见了，他去学开车了。","Kànjiàn le tā qù xué kāi chē le","Yes. He has gone to a driving lesson."),
      ("他什么时候能回来？","Tā shénme shíhou néng huílai","When can he come back?"),
      ("四十分钟后回来。","Sìshí fēnzhōng hòu huílai","After 40 minutes."),
    ]},
    {"name":"在商店门口 Outside a store","track":"14-3","sents":[
      ("王方的衣服太漂亮了！","Wáng Fāng de yīfu tài piàoliang le","Wang Fang's dress is so pretty!"),
      ("是啊，她买了不少衣服。","Shì a tā mǎile bùshǎo yīfu","Yes. She has bought quite a few clothes."),
      ("你买什么了？","Nǐ mǎi shénme le","What did you buy?"),
      ("我没买，这些都是王方的东西。","Wǒ méi mǎi zhèxiē dōu shì Wáng Fāng de dōngxi","I bought nothing. All these are Wang Fang's stuff."),
    ]},
  ]},
  # L15
  {"id":"lesson-15","title":"我是坐飞机来的","en":"I came here by air","scenes":[
    {"name":"在餐桌旁 At the dining table","track":"15-1","sents":[
      ("你和李小姐是什么时候认识的？","Nǐ hé Lǐ xiǎojiě shì shénme shíhou rènshi de","When did you and Miss Li first meet?"),
      ("我们是二零一一年九月认识的。","Wǒmen shì èr líng yī yī nián jiǔ yuè rènshi de","We met in September, 2011."),
      ("你们在哪儿认识的？","Nǐmen zài nǎr rènshi de","Where did you meet each other?"),
      ("我们是在学校认识的，她是我大学同学。","Wǒmen shì zài xuéxiào rènshi de tā shì wǒ dàxué tóngxué","We met in our university. She was my classmate."),
    ]},
    {"name":"在饭店门口 Outside a hotel","track":"15-2","sents":[
      ("你们是怎么来饭店的？","Nǐmen shì zěnme lái fàndiàn de","How did you come here?"),
      ("我们是坐出租车来的。","Wǒmen shì zuò chūzūchē lái de","We came by taxi."),
      ("李先生呢？","Lǐ xiānsheng ne","What about Mr. Li?"),
      ("他是和朋友一起开车来的。","Tā shì hé péngyou yìqǐ kāi chē lái de","He drove here with his friend."),
    ]},
    {"name":"在公司 In the company","track":"15-3","sents":[
      ("很高兴认识您！李小姐。","Hěn gāoxìng rènshi nín Lǐ xiǎojiě","Nice to meet you, Miss Li."),
      ("认识你我也很高兴！","Rènshi nǐ wǒ yě hěn gāoxìng","Nice to meet you too."),
      ("听张先生说，您是坐飞机来北京的？","Tīng Zhāng xiānsheng shuō nín shì zuò fēijī lái Běijīng de","Mr. Zhang said you came to Beijing by plane, didn't you?"),
      ("是的。","Shì de","Yes, I did."),
    ]},
  ]},
]
