import csv
import random

# Bangladesh-specific spam patterns - real problems
spam_patterns = [
    # Lottery/Prize scams
    "আপনার মোবাইল নম্বর {company} লটারিতে বিজয়ী হয়েছে! {amount} টাকা জিতেছেন। কল করুন: {phone}",
    "অভিনন্দন! আপনি {company} এর {prize} জিতেছেন। দাবি করতে {phone} নম্বরে কল করুন।",
    "প্রিয় গ্রাহক, আপনার নাম্বার র্যান্ডম ড্র তে নির্বাচিত। পুরস্কার {amount} টাকা। কল: {phone}",
    # Fake banking/payment alerts
    "আপনার {bank} একাউন্ট থেকে {amount} টাকা উত্তোলন হয়েছে। বন্ধ করতে {phone} এ কল করুন।",
    "{bank} alert: আপনার একাউন্ট সাসপেন্ড হতে পারে। ভেরিফাই করুন: {link}",
    "জরুরি! {bank} কার্ড ব্লক হবে। তথ্য আপডেট করুন {phone}",
    "আপনার বিকাশ একাউন্ট থেকে {amount} টাকা ডেবিট। বাতিল করতে {phone} এ কল দিন।",
    "নগদ/রকেট একাউন্ট ভেরিফিকেশন জরুরি। {phone} নম্বরে কল করুন এখনই।",
    # Loan offers
    "ঋণ পাবেন মাত্র {hour} ঘন্টায়! কোন কাগজপত্র লাগবে না। {amount} টাকা পর্যন্ত। কল: {phone}",
    "ইন্সট্যান্ট লোন সার্ভিস। {amount} টাকা পাবেন {hour} ঘন্টায়। আবেদন করুন: {phone}",
    "{company} থেকে পার্সোনাল লোন। সুদের হার মাত্র {percent}%। যোগাযোগ: {phone}",
    "জমি বন্ধক রেখে ঋণ নিন। সহজ শর্তে {amount} টাকা। কল করুন {phone}",
    # Job/earning scams
    "ঘরে বসে মাসে {amount} টাকা আয়। কোন বিনিয়োগ লাগবে না। হোয়াটসঅ্যাপ: {phone}",
    "অনলাইনে কাজ করে দৈনিক {amount} টাকা আয়। রেজিস্ট্রেশন ফি মাত্র {fee} টাকা। {phone}",
    "বিদেশে চাকরির সুযোগ। স্যালারি {amount} টাকা। ভিসা গ্যারান্টি। যোগাযোগ: {phone}",
    "পার্ট টাইম জব। দিনে {hour} ঘন্টা কাজ করে {amount} টাকা আয়। কল: {phone}",
    "মোবাইল রিচার্জ এর ব্যবসা শুরু করুন। বিনিয়োগ {investment} টাকা। লাভ {percent}%। {phone}",
    # E-commerce/product offers
    "বিশেষ অফার! {product} মাত্র {price} টাকায়। ফ্রি হোম ডেলিভারি। অর্ডার: {phone}",
    "{percent}% ছাড়ে {product} কিনুন। লিমিটেড স্টক। {company} অর্ডার করুন: {phone}",
    "{product} এর দাম কমেছে {percent}%। ক্যাশ অন ডেলিভারি। কল করুন: {phone}",
    "অরিজিনাল {product} সস্তায় পাবেন। ঢাকার বাহিরে কুরিয়ার ফ্রি। {phone}",
    # Mobile operator fake offers
    "{operator} অফার: আনলিমিটেড ইন্টারনেট মাত্র {price} টাকায়। SMS YES {code}",
    "প্রিয় {operator} গ্রাহক, আপনি পাচ্ছেন {gb}GB ফ্রি। অ্যাক্টিভ করতে কল দিন {phone}",
    "{operator} থেকে ফ্রি {amount} টাকা রিচার্জ পাবেন। নিতে SMS করুন {code}",
    # Investment scams
    "{company} তে বিনিয়োগ করুন। মাসিক লাভ {percent}%। মিনিমাম {investment} টাকা। {phone}",
    "ক্রিপ্টো কারেন্সি ট্রেডিং শিখুন। দৈনিক {amount} টাকা আয়। রেজিস্টার করুন: {link}",
    "শেয়ার বাজারে বিনিয়োগ করুন। {percent}% রিটার্ন গ্যারান্টি। কল: {phone}",
    # Health/medicine scams
    "{medicine} ট্যাবলেট মাত্র {price} টাকা। ১০০% কার্যকর। হোম ডেলিভারি। অর্ডার: {phone}",
    "দ্রুত ওজন কমান। {medicine} ব্যবহার করুন। গ্যারান্টি সহ। মূল্য {price} টাকা। {phone}",
    # Real estate scams
    "জমি কিনুন সস্তায়। {location} এ প্লট মাত্র {price} টাকা। বুকিং {deposit} টাকা। {phone}",
    "ফ্ল্যাট বুকিং চলছে। {location} এ {size} বর্গফুট। মূল্য {price} টাকা। যোগাযোগ: {phone}",
    # Fake government schemes
    "সরকারি স্কিম: {amount} টাকা অনুদান পাবেন। আবেদন ফি {fee} টাকা। কল করুন {phone}",
    "প্রধানমন্ত্রীর বিশেষ প্যাকেজ। {amount} টাকা সহায়তা। রেজিস্ট্রেশন: {phone}",
    # Promotional spam (legitimate but promotional)
    "আজই শেষ সুযোগ! ভিতুন {amount} বোনাস মেম্বারশিপ রিওয়ার্ডস পয়েন্টস নূনতম {count}টি কেনাকাটা করে {date}-{date} নভেম্বর {year}-এর মধ্যে আপনার আমেক্স ক্রেডিট কার্ড দিয়ে। শর্ত প্রযোজ্য। বিস্তারিত {link}",
    "foodpanda-তে {count} ও ৬ ডিসেম্বর 'AMEX200' ব্যবহার করে উপভোগ করুন ২০০ টাকা পর্যন্ত সাশ্রয়। শর্ত প্রযোজ্য। বিস্তারিত {link}",
    "{amount} ডলার এনডোর্স করে উপভোগ করুন {amount} পর্যন্ত বোনাস এক্স আর পয়েন্টস ! বিস্তা: {link}",
    "আপনার আমেক্স ক্রেডিট কার্ড দিয়ে {date} ডিসেম্বর {year}-এর মধ্যে নূনতম {count}টি কেনাকাটা করে জিতুন {amount} বোনাস মেম্বারশিপ রিওয়ার্ডস পয়েন্টস! শর্ত প্রযোজ্য। বিস্তারিত: {link}",
    # Fashion/Shopping spam
    "ঈজি ফ্যাশনে নতুন ডিজাইনের ঈদ কালেকশন সকাল শাখায় {link}",
    "ঈদ উপলক্ষে আহয়া কালেকশন এখন ঈজি ফ্যাশনের সকাল শাখায়। {link}",
    "ঈজি ফ্যাশনের ঈদ উপহার নির্দিষ্ট পন্য আকর্ষনীয় ছাড় {link}",
    "শীতের নতুন কালেকশন এখন ঈজি ফ্যাশনের সকল শোরুমে। {link}",
    # Lottery/Bonus spam
    "{amount} টাকা বোনাস জিতেছে আপনি ইনস্টল করুন:{link}",
    "কোডে! মিস করবেন? ভিজিট- {link} রকমারি",
    "আখেরি অফার বইয়ের {percent}% ছাড়, আর্পে {percent}% এক্সট্রা ছাড় - {link} রকমারি",
    "আজই শেষ হচ্ছে যে বিশেষ অফার!* বিস্তারিত জানতে- {link} রকমারি।",
    "রকমারি ফ্রি বই ও ফ্রি পিপির! আজ বিকেল ৩-৫ টা BUYDAY কোডে* - {link}",
    # News/Breaking news spam
    "<<ব্রেকিং নিউজ>> কারাগার থেকে সেনানিবাসের সার্জেল ১৫ সেনা কর্মকর্তা..প্রতিদিন ১,৩৯ টাকা. এই ধরনের সর্বশেষ খবরগুলো পেতে {link}",
    # Ticket booking spam
    "ভর্তি পরীক্ষার যাতায়াতের বাস টিকেট কাটতে ক্লিক: {link} কল ১৬৪৬০",
    "বাসের প্রতি টিকেটে ৮৫০ ছাড় কোড: 50TK0FF ক্লিক: {link} কল: ১৬৪৬০",
    "নিরাপদে বাড়ি ফিরুন, ঝামেলাহীন বাস টিকেট পেতে ক্লিক: {link}",
    # Generic promotional with links
    "প্রোগ্রামিং শেখার বই অর্ডার এক্সট্রা ২০% ছাড়! লিংক- {link}",
    "নির্ভরযোগ্য উপহার,ফ্রি সিপিং,{percent}% ছাড়- ইন্দি অফারে- {link}",
    "৩০-৭০% ছাড় {percent}% ক্যাশব্যাক রিয়েলেস সেল আজই শেষ* রকমারি - {link}",
]

# Real ham patterns from Bangladesh
ham_patterns = [
    # Family conversations
    "আম্মু, আজ রাতে বাসায় খাবো না। তুমি খেয়ে নিও।",
    "বাবা, আমার একটু টাকা দরকার। পাঠাতে পারবে?",
    "আপু, তুমি কখন বাসায় আসবে? আমার একটা কাজ ছিল।",
    "ভাই, মায়ের ওষুধ কিনে আনতে হবে। তুমি কি নিয়ে আসতে পারবে?",
    "ছোট ভাই, তোর পরীক্ষা কেমন হলো? রেজাল্ট কবে দিবে?",
    "মা, আজ অফিস থেকে একটু দেরি হবে। তুমি ঘুমিয়ে পড়ো।",
    "আব্বু, আমি ঢাকা পৌঁছে গেছি। চিন্তা করবেন না।",
    # Friends/social
    "কি রে, কেমন আছিস? অনেক দিন দেখা নেই।",
    "আজ সন্ধ্যায় বাসায় থাকলে একটু আসবো। ঠিক আছে?",
    "দোস্ত, কাল ক্রিকেট খেলা আছে। আসবি তো?",
    "ভাই, তোর বাইকটা কি আজকে নিতে পারি? আমার একটা কাজ আছে।",
    "আজ রাতে গল্পের অ্যাডা আছে চা-স্টলে। আসবা?",
    "কিরে, কবে দেখা হবে? অনেক দিন হয়ে গেলো তো।",
    "তুই কি আজকে ক্লাসে এসেছিলি? নোটস দিতে পারবি?",
    # Work/professional
    "স্যার, আজ আমি একটু অসুস্থ। অফিসে আসতে পারবো না।",
    "বস, মিটিংটা কয়টায়? আমি রেডি আছি।",
    "ভাই, কালকের রিপোর্টটা কি জমা দিয়েছো? ডেডলাইন তো আজ।",
    "স্যার, আমার স্যালারি এখনো একাউন্টে আসেনি। একটু চেক করে দেখবেন?",
    "আপা, আজকের মিটিং কি ক্যান্সেল হয়েছে? একটু জানাবেন প্লিজ।",
    # Daily life/practical
    "ভাইয়া, বাসায় কেউ আছে? আমি দরজায় দাঁড়িয়ে আছি।",
    "আজ বাজার করে আনবো। কি কি লাগবে বলে দাও।",
    "গ্যাস শেষ হয়ে গেছে। নতুন সিলিন্ডার অর্ডার দিতে হবে।",
    "বিদ্যুৎ চলে গেছে। জেনারেটর চালু করা দরকার।",
    "আজ অনেক জ্যাম আছে। আমি একটু দেরি করে পৌঁছাবো।",
    "ফোনে চার্জ নেই। একটু পরে কল করছি।",
    "দোকানটা কয়টা পর্যন্ত খোলা থাকে? আমি যাচ্ছি।",
    # Greetings/occasions
    "ঈদ মুবারক! তুমি কেমন আছো?",
    "জন্মদিনের অনেক অনেক শুভেচ্ছা! আল্লাহ তোমার মঙ্গল করুন।",
    "বিজয় দিবসের শুভেচ্ছা। জয় বাংলা!",
    "নতুন বছরের শুভেচ্ছা। নতুন বছর সবার জন্য মঙ্গলময় হোক।",
    # Health/care
    "তোমার শরীর কেমন? ডাক্তার কি বলেছে?",
    "ওষুধ খেয়েছো? ঠিক সময়ে খাবে কিন্তু।",
    "আজ হাসপাতালে যাবো। তুমি কি সাথে আসতে পারবে?",
    "ডাক্তারের অ্যাপয়েন্টমেন্ট কাল সকাল ১০টায়। ভুলে যাবে না।",
    # Education
    "আজকের ক্লাস কয়টায়? আমি ভুলে গেছি।",
    "পরীক্ষার রুটিন কি বের হয়েছে? একটু পাঠাতে পারবে?",
    "অ্যাসাইনমেন্ট জমা দেওয়ার শেষ তারিখ কবে?",
    "লাইব্রেরি কয়টা পর্যন্ত খোলা? আমার পড়তে যেতে হবে।",
    # Food/restaurant
    "আজ রাতে কি রান্না করবে? খিদে পেয়েছে।",
    "বাইরে থেকে খাবার অর্ডার দেবো? তুমি কি খাবে?",
    "বিরিয়ানি খাবে? আমি অর্ডার দিচ্ছি।",
    "চা বানিয়ে দাও তো। খুব ঘুম পাচ্ছে।",
    # Shopping
    "বাজারে পেঁয়াজের দাম কত? অনেক বেড়েছে নাকি?",
    "নতুন জামা কিনবো। তুমি কি সাথে যাবে?",
    "তোমার জুতা কোথা থেকে কিনেছিলে? দামটা কত ছিল?",
    "মোবাইল শপে নতুন ফোন এসেছে। একটু দেখে আসবো।",
    # Transport
    "আজ ট্রেন ধরতে হবে। স্টেশনে পৌঁছাতে কতক্ষণ লাগবে?",
    "বাসে উঠেছি। আধা ঘন্টার মধ্যে পৌঁছাবো।",
    "আজ উবার নেবো নাকি সিএনজিতে যাবো?",
    "রিক্সা পাচ্ছি না। তুমি কি পিক করতে পারবে?",
    # Weather/environment
    "আজ অনেক গরম। এসি চালাতে হবে।",
    "বৃষ্টি হচ্ছে। ছাতা নিয়ে বের হবে।",
    "আজ কুয়াশা অনেক। গাড়ি চালাতে সাবধান থাকবে।",
    "তুমি কি জানো কাল থেকে ঠাণ্ডা পড়বে?",
    # Banking/financial (legitimate)
    "আমার একাউন্ট নাম্বার দরকার। পাঠাতে পারবে?",
    "বিকাশে টাকা পাঠাও। আমার নাম্বার জানো তো?",
    "টাকাটা পেয়েছি। ধন্যবাদ ভাই।",
    "দোকানের ভাড়া দিতে হবে। টাকা রেডি রেখো।",
    # Technology
    "তোমার ওয়াইফাই পাসওয়ার্ড কি? আমার ইন্টারনেট নেই।",
    "ফোনটা হ্যাং করছে। রিস্টার্ট দিতে হবে।",
    "ল্যাপটপ চার্জার নিয়ে আসবে? আমার দরকার।",
    "তোমার ফোন নাম্বার সেভ হয়নি। আবার দাও তো।",
    # Mobile operator legitimate messages
    "সময় 00:00:12,কাটা হয়েছে 0.17 Taka,বর্তমান ব্যালেন্স 38.22 Taka",
    "সময় 00:00:37,কাটা হয়েছে 0.51 Taka,বর্তমান ব্যালেন্স 37.71 Taka",
    # bKash legitimate transactions
    "You have received Tk 72.00 from 01773448862. Fee Tk 0.00. Balance Tk 11,562.48. TrxID CKJ6C7KUN4 at 19/11/2025 12:00",
    "You have received Tk 1,100.00 from 01859845470. Fee Tk 0.00. Balance Tk 8,982.48. TrxID CK00HI24BI at 24/11/2025 18:21",
    "Your bKash verification code is 840223. The code will expire in 2 minutes. Please do NOT share your OTP or PIN with others.",
    "Payment of Tk 800.00 to ICC Communication is successful. Balance Tk 3,052.48. TrxID CL31Q0UTRT at 03/12/2025 00:20",
    "Bill successfully paid. Biller: ICCComm MMYYYY/Contact: 01721170869 A/C: 73054 Amount: Tk 600.00 Fee: Tk 0.00 TrxID: CL85VHUJ0X at 08/12/2025 13:25",
    "Bill successfully paid. Biller: WZPDCL MMYYYY/Contact: 112025 A/C: 201129120 Amount: Tk 1,448.00 Fee: Tk 0.00 TrxID: CL88VHVQS0 at 08/12/2025 13:26",
    "You have received Tk 100.00 from 01859845470. Fee Tk 0.00. Balance Tk 8,107.39. TrxID BKK1FD0EB9 at 20/11/2024 20:41",
    "You have received remittance. Total: Tk 12,402.50 Govt. incentive: Tk 302.50 TrxID BKM3GGEY3F at 22/11/2024 09:33.",
    "Bill successfully paid. Biller: WZPDCL MMYYYY/Contact: 102024 A/C: 201129120 Amount: Tk 1,846.00 Fee: Tk 0.00 TrxID: BKN7HQ5RTN at 23/11/2024",
    # Bank legitimate messages
    "Your JBPLC. account *5877 credited with BDT 1000.00 from Medical College at 03 Jul 25 14:18:52 Balance is BDT 1040 . Enjoy Amar Sanchoy Amar Munafa",
    "Your JBPLC. account *5877 credited with BDT 1000.00 from Barisal Corporate at 06 Aug 25 13:39:33 Balance is BDT 1040 .",
    "Dear Sir, your JBPLC. A/C **5451 has been credited (Interest) by BDT2583.66 on 10-SEP-2025. C/B is BDT0. Use eJanata app for i-banking. Thanks",
    "Your JBPLC. account *5877 debited with BDT40.00 from Alinagar at 11 Sep 25 12:11:44 Balance is BDT 0 . Enjoy A-Challan from any branch",
    "Dear Sir, Your SMS Alert Mobile number has been changed from 01712911614 to 01721170869 at Janata Bank PLC. You will now receive SMS on the new number. Thank You.",
    "Your JBPLC. ATM Card No.7012***4920 debited with BDT20015.00. Balance is BDT14646.31. at 02 Dec 25 17:44:55 from Barishal ATM. Visit www.jb.com.bd for services",
    "Your OTP is 708411. It will be valid for 3 minutes. Never share OTP, PIN, CVV, Expiry Date and Password with anyone. TBL-Digital Banking.",
    # bKashCS service messages
    "Your Service Request Number is 8953. Please do not share it with anyone except bKash Customer Service Executive of bKash Grahok Sheba or livechat.bkash.com.",
    "শুধুমাত্র বিকাশ লাইভচ্যাট স্ক্রিনে সার্ভিস রিকোয়েস্ট নাম্বার 021065 লিখুন। কল বা SMS এর মাধ্যমে নাম্বারটি কারো সাথে শেয়ার করবেন না।",
    # Government information messages
    "আজ ২৩ মে ২০২৪, বিশ্ব মেটেলিজি দিবস। এবারের প্রতিপাদ্য- 'টেকসই ভবিষ্যৎ বিনির্মাণে আজকের পরিমাপ', থিএসচিআই, শিল্প মন্ত্রণালয়।",
    '"অর্থনৈতিক শুমারি ২০২৪ এর আওতায় দেশের সকল খানা ও প্রতিষ্ঠান তালিকাভুক্ত করা হচ্ছ। জাতীয় স্বার্থপূর্ণ এ কার্যক্রমে আপনার তথ্য দিয়ে সহযোগিতা করুন" - বাংলাদেশ পরিসংখ্যান ব্যুরো।',
    "বাংলাদেশ নৌবাহিনীতে অফিসার ক্যাডেট পদে নিয়োগ চলছে। ভিজিট করুন: http://joinnavy.navy.mil.bd",
    '২২ সেপ্টেম্বর ২০২৯ "বিশ্ব ব্যক্তিগত গাড়িমুক্ত দিবস"। "গণপরিবহনে ও হেঁটে চলি, ব্যক্তিগত গাড়ি সীমিত করি"-ডিটিসিএ।',
    # FlexiLoad/Recharge confirmations
    "You have Successfully recharged with amount 20.00 BDT.Transaction ID is BD030225192022138766. Visit MyGP to get attractive cashback on recharge https://mygp.li/sn",
    # Shukhee verification
    "shukhee Confirmation Code:9299 (Please do not share this code with anyone else)",
]


def generate_spam_message():
    template = random.choice(spam_patterns)

    companies = [
        "গ্রামীণফোন",
        "রবি",
        "বাংলালিংক",
        "টেলিটক",
        "বিকাশ",
        "নগদ",
        "রকেট",
        "ডাচ-বাংলা ব্যাংক",
        "CITY_AMEX",
    ]
    banks = [
        "ডাচ-বাংলা ব্যাংক",
        "ব্র্যাক ব্যাংক",
        "ইসলামী ব্যাংক",
        "এবি ব্যাংক",
        "সিটি ব্যাংক",
        "বিকাশ",
        "নগদ",
        "JANATA BANK",
        "TrustBank",
    ]
    products = [
        "আইফোন",
        "স্মার্টফোন",
        "ল্যাপটপ",
        "টিভি",
        "ফ্রিজ",
        "এসি",
        "মোবাইল",
        "ট্যাবলেট",
        "ওয়াচ",
        "জামা",
        "জুতা",
    ]
    prizes = [
        "বাইক",
        "গাড়ি",
        "স্মার্টফোন",
        "ল্যাপটপ",
        "উমরাহ প্যাকেজ",
        "গোল্ড কয়েন",
        "মেম্বারশিপ রিওয়ার্ডস",
    ]
    medicines = ["সেক্স পাওয়ার", "হাইট ইনক্রিজ", "ওজন কমানোর", "চুল পড়া বন্ধ"]
    locations = [
        "ধানমন্ডি",
        "গুলশান",
        "বনানী",
        "উত্তরা",
        "মিরপুর",
        "বসুন্ধরা",
        "চট্টগ্রাম",
        "সিলেট",
    ]
    operators = ["গ্রামীণফোন", "রবি", "বাংলালিংক", "টেলিটক"]
    dates = ["15-21", "1-7", "21-25", "5-10"]
    years = ["2025", "2026"]
    counts = [1, 2, 3, 5, 10]

    message = template.format(
        phone=f"0{random.randint(1500000000, 1999999999)}",
        amount=random.choice(
            [5000, 10000, 25000, 50000, 100000, 200000, 500000, 1000000, 5000000]
        ),
        percent=random.choice([5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80, 90]),
        product=random.choice(products),
        prize=random.choice(prizes),
        price=random.choice([999, 1500, 2500, 3999, 4999, 9999, 15000, 25000]),
        code=random.randint(1000, 99999),
        hour=random.choice([1, 2, 3, 6, 12, 24, 48]),
        company=random.choice(companies),
        bank=random.choice(banks),
        link=f"bit.ly/{random.randint(10000, 99999)}",
        medicine=random.choice(medicines),
        location=random.choice(locations),
        size=random.choice([650, 850, 1000, 1200, 1400, 1600]),
        deposit=random.choice([50000, 100000, 200000, 500000]),
        fee=random.choice([200, 300, 500, 1000, 2000]),
        investment=random.choice([5000, 10000, 20000, 50000, 100000]),
        operator=random.choice(operators),
        gb=random.choice([1, 2, 3, 5, 10, 15, 20]),
        date=random.choice(dates),
        year=random.choice(years),
        count=random.choice(counts),
    )
    return message


def generate_ham_message():
    return random.choice(ham_patterns)


# Generate unique messages
spam_messages = set()
ham_messages = set()

# Generate 1050 unique spam messages (35%)
print("Generating spam messages...")
while len(spam_messages) < 1050:
    msg = generate_spam_message()
    spam_messages.add(msg)
    if len(spam_messages) % 100 == 0:
        print(f"Spam: {len(spam_messages)}/1050")

# Generate 1950 unique ham messages (65%)
print("Generating ham messages...")
while len(ham_messages) < 1950:
    msg = generate_ham_message()
    ham_messages.add(msg)
    if len(ham_messages) % 100 == 0:
        print(f"Ham: {len(ham_messages)}/1950")

# Combine and shuffle
data = [{"label": "spam", "text": msg} for msg in spam_messages]
data.extend([{"label": "ham", "text": msg} for msg in ham_messages])
random.shuffle(data)

# Save to CSV
with open("bangla_sms_dataset.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["label", "text"])
    writer.writeheader()
    writer.writerows(data)

print(f"\n✅ Dataset created successfully!")
print(f"Total messages: {len(data)}")
print(f"Spam: {len(spam_messages)} (35%)")
print(f"Ham: {len(ham_messages)} (65%)")
print(f"All messages are unique!")
