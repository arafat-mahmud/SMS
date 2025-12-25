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
    # bKash/Mobile Banking phishing scams
    "আপনার বিকাশ একাউন্টে সন্দেহজনক কার্যক্রম ধরা পড়েছে। যাচাই করুন: {link}",
    "নিরাপত্তার কারণে আপনার একাউন্ট সাময়িকভাবে স্থগিত। ভেরিফাই করুন: {phone}",
    "তথ্য যাচাই না করলে একাউন্ট বন্ধ হয়ে যাবে। লিংক: {link}",
    "আপনার একাউন্ট ভেরিফিকেশন অসম্পূর্ণ রয়েছে। সম্পূর্ণ করুন: {link}",
    "আজ রাত ১২টার মধ্যে ভেরিফাই করুন। কল: {phone}",
    "নতুন ডিভাইস থেকে লগইন চেষ্টা করা হয়েছে। নিরাপত্তা যাচাই: {link}",
    "নিরাপত্তা আপডেট সম্পন্ন হয়নি। আপডেট করুন: {link}",
    "আপনার একাউন্ট ঝুঁকিপূর্ণ হিসেবে চিহ্নিত। তথ্য দিন: {phone}",
    "পরিচয় নিশ্চিত করতে লিংকে যান: {link}",
    "ওটিপি ছাড়া একাউন্ট অ্যাক্সেস সম্ভব নয়। OTP শেয়ার করুন: {phone}",
    "একাধিক ভুল চেষ্টার কারণে একাউন্ট লক। আনলক করুন: {link}",
    "তথ্য আপডেট না করলে সেবা বন্ধ হবে। আপডেট: {link}",
    "আপনার একাউন্ট রিভিউতে রয়েছে। যাচাই করুন: {phone}",
    "অস্বাভাবিক লেনদেন শনাক্ত করা হয়েছে। নিশ্চিত করুন: {link}",
    "একাউন্ট পুনরুদ্ধারের আবেদন করুন। ভিজিট: {link}",
    "নিরাপত্তা যাচাই ব্যর্থ হয়েছে। পুনরায় চেষ্টা: {link}",
    "একাউন্ট আনলক করতে এখনই ভিজিট করুন: {link}",
    "আপনার প্রোফাইল মিলছে না। তথ্য আপডেট: {phone}",
    "পরিচয় যাচাই প্রয়োজন। যাচাই করুন: {link}",
    "একাউন্ট স্থিতি: অপেক্ষমাণ। সক্রিয় করুন: {link}",
    # SIM verification/deactivation scams
    "আপনার সিম আজ ডিঅ্যাক্টিভ হতে যাচ্ছে। রক্ষা করুন: {link}",
    "সিম ভেরিফিকেশন সম্পন্ন হয়নি। এখনই করুন: {phone}",
    "কল ও ইন্টারনেট বন্ধ হওয়ার ঝুঁকি। ভেরিফাই করুন: {link}",
    "সিম পুনরায় চালু করতে তথ্য দিন: {link}",
    "জাতীয় পরিচয়পত্র যাচাই প্রয়োজন। যাচাই: {link}",
    "আপনার নম্বর ব্লক লিস্টে যাচ্ছে। রক্ষা করুন: {phone}",
    "সিম রেজিস্ট্রেশন আপডেট করুন। লিংক: {link}",
    "আজই ভেরিফাই না করলে সেবা বন্ধ। ভেরিফাই: {link}",
    "সিম মালিকানা নিশ্চিত করুন। কল: {phone}",
    "সিম সংক্রান্ত জরুরি নোটিস। লিংক: {link}",
    # Parcel/delivery scams
    "আপনার পার্সেল ডেলিভারি ব্যর্থ হয়েছে। ট্র্যাক করুন: {link}",
    "ঠিকানা অসম্পূর্ণ থাকায় ডেলিভারি হয়নি। আপডেট: {link}",
    "পার্সেল হাবে আটকে আছে। ছাড়পত্রের জন্য: {link}",
    "আজ শেষ ডেলিভারি চেষ্টা। ঠিকানা দিন: {phone}",
    "ঠিকানা আপডেট না করলে পার্সেল ফেরত। আপডেট: {link}",
    "ডেলিভারি কনফার্মেশন প্রয়োজন। কনফার্ম করুন: {link}",
    "আপনার পার্সেল অপেক্ষমাণ। ডেলিভারি নিন: {link}",
    "কুরিয়ার যোগাযোগ করতে পারেনি। যোগাযোগ: {phone}",
    "পার্সেল ছাড়পত্র প্রয়োজন। পেমেন্ট: {link}",
    "ডেলিভারি চার্জ বকেয়া। পরিশোধ করুন: {link}",
    # Lucky draw/prize scams
    "আপনি লাকি ড্রতে নির্বাচিত হয়েছেন। {amount} টাকা জিতেছেন! দাবি: {link}",
    "আপনার জন্য পুরস্কার অপেক্ষা করছে। গ্রহণ করুন: {link}",
    "আজই পুরস্কার দাবি করুন। শেষ সুযোগ: {phone}",
    "পুরস্কার গ্রহণের সময়সীমা শেষ হচ্ছে। দ্রুত করুন: {link}",
    "আপনার নাম বিজয়ী তালিকায়। {prize} পাবেন! লিংক: {link}",
    "গিফট পাঠানোর জন্য তথ্য দিন: {link}",
    "ফ্রি উপহার জিতেছেন আপনি। দাবি করুন: {link}",
    "পুরস্কার ডেলিভারি স্থগিত। তথ্য দিন: {phone}",
    "আজ শেষ সুযোগ। {amount} টাকা জিতুন: {link}",
    "পুরস্কার কনফার্মেশন প্রয়োজন। কনফার্ম: {link}",
    # Instant loan scams
    "আপনি প্রি-অ্যাপ্রুভড লোন পেয়েছেন। {amount} টাকা নিন: {link}",
    "কোনো কাগজপত্র ছাড়াই লোন নিন। আবেদন: {link}",
    "আজই লোন অ্যাপ্রুভাল। {amount} টাকা পান: {phone}",
    "জরুরি টাকার সমাধান এখনই। লোন নিন: {link}",
    "কম সুদে লোন সুবিধা। মাত্র {percent}% সুদ। আবেদন: {link}",
    "আপনার লোন আবেদন অনুমোদিত। {amount} টাকা পাবেন: {link}",
    "লোন রিলিজের জন্য তথ্য দিন: {phone}",
    "আজই টাকা আপনার একাউন্টে। {amount} টাকা নিন: {link}",
    "সীমিত সময়ের লোন অফার। {amount} টাকা পর্যন্ত: {link}",
    "লোন কনফার্মেশন বাকি। কনফার্ম করুন: {link}",
    # Work from home/earning scams
    "ঘরে বসে আয় করার সুযোগ। দৈনিক {amount} টাকা: {link}",
    "প্রতিদিন আয় করুন মোবাইল দিয়ে। রেজিস্ট্রার: {link}",
    "কোনো অভিজ্ঞতা ছাড়াই কাজ। আয় করুন: {link}",
    "দিনে {amount} টাকা আয় সম্ভব। শুরু করুন: {link}",
    "অনলাইন কাজের সুযোগ। মাসিক {amount} টাকা: {phone}",
    "ফ্রি রেজিস্ট্রেশন আজই। আয় শুরু করুন: {link}",
    "সহজ কাজ, দ্রুত পেমেন্ট। জয়েন করুন: {link}",
    "পার্ট-টাইম ইনকাম সুযোগ। {amount} টাকা আয়: {link}",
    "বিশ্বস্ত আয়ের প্ল্যাটফর্ম। শুরু করুন: {link}",
    "আজই কাজ শুরু করুন। {amount} টাকা আয়: {link}",
    # Social media account phishing
    "আপনার ফেসবুক একাউন্ট রিপোর্ট হয়েছে। যাচাই করুন: {link}",
    "ফেসবুক ভেরিফিকেশন প্রয়োজন। ভেরিফাই করুন: {link}",
    "একাউন্ট স্থগিত হওয়ার ঝুঁকি। রক্ষা করুন: {link}",
    "কপিরাইট সমস্যা ধরা পড়েছে। সমাধান করুন: {link}",
    "একাউন্ট রিকভারি দরকার। রিকভার করুন: {link}",
    "নিরাপত্তা যাচাই সম্পন্ন হয়নি। যাচাই করুন: {link}",
    "ফেসবুক একাউন্ট সীমিত করা হয়েছে। আনলক: {link}",
    "পরিচয় নিশ্চিত করুন। ভেরিফাই: {link}",
    "আজ ভেরিফাই না করলে একাউন্ট বন্ধ: {link}",
    "একাউন্ট রিস্টোর করার আবেদন করুন: {link}",
    # WhatsApp phishing
    "আপনার হোয়াটসঅ্যাপ একাউন্ট ঝুঁকিতে। সুরক্ষা করুন: {link}",
    "অস্বাভাবিক লগইন শনাক্ত। যাচাই করুন: {link}",
    "হোয়াটসঅ্যাপ নিরাপত্তা আপডেট প্রয়োজন: {link}",
    "একাউন্ট সাময়িকভাবে সীমিত। আনলক: {link}",
    "আজই যাচাই করুন। একাউন্ট রক্ষা করুন: {link}",
    "একাউন্ট স্থায়ীভাবে বন্ধ হতে পারে: {link}",
    "পরিচয় নিশ্চিত করা জরুরি। ভেরিফাই: {link}",
    "হোয়াটসঅ্যাপ নোটিস। দ্রুত পদক্ষেপ নিন: {link}",
    "নিরাপত্তা সতর্কতা। ক্লিক করুন: {link}",
    "একাউন্ট ভেরিফিকেশন বাকি। সম্পূর্ণ করুন: {link}",
    # Instagram phishing
    "ইনস্টাগ্রাম একাউন্ট যাচাই প্রয়োজন: {link}",
    "আপনার প্রোফাইল রিপোর্ট হয়েছে। যাচাই করুন: {link}",
    "একাউন্ট রিভিউ চলছে। তথ্য দিন: {link}",
    "ভেরিফিকেশন ব্যাজের আবেদন অনুমোদিত: {link}",
    "আজ কনফার্ম না করলে বাতিল: {link}",
    "ইনস্টাগ্রাম একাউন্ট সীমাবদ্ধ: {link}",
    "নীতিমালা লঙ্ঘন ধরা পড়েছে। সমাধান: {link}",
    "একাউন্ট পুনরুদ্ধারের সুযোগ: {link}",
    "প্রোফাইল যাচাই করুন: {link}",
    "ইনস্টাগ্রাম সতর্কবার্তা। দ্রুত পদক্ষেপ: {link}",
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
    # GP Wishes and Greetings
    "৮ বছর আগে আজকের দিনেই শুরু হয়েছিল গ্রামীণফোনের সাথে আপনার পথচলা। আশা করি আগামী দিনগুলো হবে আরো সুন্দর ও সন্তুষ্টিবনাময়।",
    "৯ বছর আগে আজকের দিনেই শুরু হয়েছিল গ্রামীণফোনের সাথে আপনার পথচলা। আশা করি আগামী দিনগুলো হবে আরো সুন্দর ও সন্তুষ্টিবনাময়।",
    # SmartGames promotional
    "মাত্র ৩ টাকায় রেইন গেমস খেলুন High Fives এ! খেলতে ক্লিক: https://cutt.ly/smartgamezz ; ট্যাক্সসহ চার্জ ৩.০৩ টাকা/দিন",
    "মাত্র ৩ টাকায় রেইন গেমস খেলুন High Fives এ! খেলতে ক্লিক: https://cutt.ly/Cehcak9l ; ট্যাক্সসহ চার্জ ৩.০৩ টাকা/দিন।",
    # ExtraOffer
    "বিকাশ/নগদ/উপায়/রকেট থেকে আজ রবিতে ৮৩৯৮রিচার্জে ১৮জিবি ও ৮৪৪৮রিচার্জে ২৮জিবি! মেয়াদ ৩০দিন",
    # Big Sale
    "সীমিত সময়ের জন্য সেরা অফার, মাত্র ৮১৪-২জিবি-১দিন নিতে ডায়াল *২১২*১৪#",
    # Best_Deal
    "আজ থেকোনো নং-এ ২টাকার কথা বলুনেই ১প/সে(+ট্যাক্স) কলরেট, মেয়াদ ৭দিন (সর্বোচ্চ ১বার)",
    # GP RC34Tk
    "৯৯পয়সা/মিঃ কলরেট উপভোগ করুন ৩৪টাকা রিচার্জে(খরিল)।",
    # bdtickets
    "সিট কিছু শেষের দিকে! টিকেট কাটুন এখনই। cutt.ly/BePQRgZP",
    # CloudGaming
    "বাংলাদেশে প্রথমবারের মতো চলে এলো Cloud Gaming ; খেলতে ক্লিক করুন : https://cutt.ly/9eoPHFzb ; ট্যাক্সসহ চার্জ ৫.০৫ টাকা/দিন।",
    # FestiveDeal
    "আজ ৮২৯৯-২৫GB+২০০মি-০০D *২১২*৯৩#, ৮৪৯-৭GB-৭D *২১২*৯৫# (১৩-১৫)Oct ১বার",
    # GPSheraDeal
    "৪০০টাকায়। ডায়াল *২১২*৫১৪৫#, mygp.li/mo",
    "ধামাকা বোনাস অফার ৩০জিবি ৩০দিন ৪০০টাকায়। ডায়াল *২১২*৫১৪৫#, mygp.li/mo",
    "ধামাকা বোনাস অফার ৩০জিবি ৩০দিন ৪০০টাকায়।নিতে ১৭ মার্চ এর মধ্যে ডায়াল *২১২*৫১৪৫#, mygp.li/mo",
    "শুধু আজকের স্পেশাল! ১৫জিবি ১৩০টাকা ৭দিন। ডায়াল *২১২*৫০৪৭#, mygp.li/ck",
    # GP Cashback
    "নগদ থেকে জিপি নম্বরে ৫০টাকা রিচার্জে ২০টাকা ক্যাশব্যাক, সর্বোচ্চ ১বার। চলবে ৩৯আক্টোবর পর্যন্ত। ডায়াল *৩৬৭#",
    "নগদ থেকে জিপি নম্বরে ৯৭টাকা রিচার্জে ১০টাকা ক্যাশব্যাক, সাথে ২৩মিনিট ১০দিন, সর্বোচ্চ ১বার। চলবে ৩১অক্টোবর পর্যন্ত",
    "নগদ থেকে জিপি নম্বরে ১১৮টাকা রিচার্জে ১১৮টাকা ক্যাশব্যাক,সাথে ১২জিবি ৮দিন। ৪ নভেম্বর বিকাল ৪টা-রাত ১২টা,নিয়েতে ১ম জন। ডায়াল *৩৬৭#",
    "নগদ থেকে জিপি নম্বরে ১১৮টাকা রিচার্জে ১১৮টাকা ক্যাশব্যাক,সাথে ১২জিবি ৮দিন। ১৩ নভেম্বর বিকাল ৪টা-রাত ১টা। ডায়াল *৩৬৭#",
    # BTRC Official
    "প্রমোশনাল এসএমএস না চাইলে *৭# ডায়াল করে চালু করুন ডু নট ডিস্টার্ব সেবা, অন্যথায় চালু না করার অনুরোধ করা হলো : বিটিআরসি",
    "প্রমোশনাল এসএমএস না চাইলে *১২১*১১০১# ডায়াল (ফ্রি) করে চালু করুন ডু নট ডিস্টার্ব সেবা, অন্যথায় চালু না করার অনুরোধ করা হলো : বিটিআরসি",
    # gpfi Promotional
    "gpfi Unlimited এখন আপনার এলাকায় । ওয়ারলেস ওয়াই-ফাই সেবা উপভোগ করুন ইনস্টলেশন ফী ছাড়া। অর্ডার করুন: gpworld.co/gpfi_request",
    "ফাইবার কাটি এর জন্যে ইন্টারনেটের কানেকশন বিচ্ছিন্ন হওয়ার চিন্তা নেই আর! অর্ডার করুন gpfi Unlimited আজই: gpworld.co/gpfi_request",
    "gpfi Unlimited নিয়ে এলো মাসিক 'ওয়াই-ফাই' প্ল্যান! শুরু মাত্র ১০০০ টাকা থেকে! অর্ডার করুন আজই। ক্লিক: gpworld.co/gpfi_request",
    # MYGPINFO
    "আপনার NID দিয়ে কয়টি সিম রেজিস্ট্রার্ড দেখে নিতে https://mygp.li/SN",
    "আপনার NID দিয়ে কয়টি সিম রেজিস্ট্রার্ড দেখে নিতে https://mygp.li/nS",
    # GP RC159TK
    "১.২০ টাকা/মিনিট কলরেট উপভোগ করুন ১৫৯টাকা রিচার্জে মেয়াদ ৩০দিন।",
    # BAY Payment confirmation
    "Thanks for Choosing 'BAY' VN: 286221-003-86-0006 Paid: 1200 https://sales.bayerp.com/online-invoice/286221/286221-003-86-0006 C.Care: +8801709995758",
    # TWELVE Promotional
    "টুয়েলভে উইন্টার সহ সকল পণ্য ফ্ল্যাট ২৪% ছাড় ১৪ ডিসেম্বর পর্যন্ত।",
    # Additional bKash messages
    "You have received Tk 100.00 from 01859845470. Fee Tk 0.00. Balance Tk 8,107.39. TrxID BKK1FD0EB9 at 20/11/2024 20:41",
    "You have received remittance. Total: Tk 12,402.50 Govt. incentive: Tk 302.50 TrxID BKM3GGEY3F at 22/11/2024 09:33.",
    "Remittance Cash Out charge only 7 Tk/thousand from ATM Details: https://bka.sh/ATMCO",
    "Congratulations! You have received a BDT 50 Discount coupon upon receiving Remittance with bKash. Details: https://www.bkash.com/page/rem-100tk-cp-mr-pmnt Validity: 29-11-2024",
    "Congratulations! You have received a BDT 50 Mobile Recharge Coupon for receiving Remittance. Validity: 27-11-2024",
    "Bill successfully paid. Biller: WZPDCL MMYYYY/Contact: 102024 A/C: 201129120 Amount: Tk 1,846.00 Fee: Tk 0.00 TrxID: BKN7HQ5RTN at 23/11/2024",
    "You have received Tk 72.00 from 01773448862. Fee Tk 0.00. Balance Tk 11,562.48. TrxID CKJ6C7KUN4 at 19/11/2025 12:00",
    "You have received Tk 1,100.00 from 01859845470. Fee Tk 0.00. Balance Tk 8,982.48. TrxID CK00HI24BI at 24/11/2025 18:21",
    "Your bKash verification code is 840223. The code will expire in 2 minutes. Please do NOT share your OTP or PIN with others.",
    "Your bKash verification code is 295842. The code will expire in 2 minutes. Please do NOT share your OTP or PIN with others.",
    "Payment of Tk 800.00 to ICC Communication is successful. Balance Tk 3,052.48. TrxID CL31Q0UTRT at 03/12/2025 00:20",
    "Bill successfully paid. Biller: ICCComm MMYYYY/Contact: 01721170869 A/C: 73054 Amount: Tk 600.00 Fee: Tk 0.00 TrxID: CL85VHUJ0X at 08/12/2025 13:25",
    "Bill successfully paid. Biller: WZPDCL MMYYYY/Contact: 112025 A/C: 201129120 Amount: Tk 1,448.00 Fee: Tk 0.00 TrxID: CL88VHVQS0 at 08/12/2025 13:26",
    # GP 2GB 45TK offers
    "আজকের অফার! ২জিবি ৪৫টাকা ৭দিন।ডায়াল *২১২*৫৪৩০# বা https://mygp.li/Rt",
    # FlexiLoad recharge confirmations
    "You have Successfully recharged with amount 20.00 BDT.Transaction ID is BD030225192022138766. Visit MyGP to get attractive cashback on recharge https://mygp.li/sn",
    "You have Successfully recharged with amount 20.00 BDT.Transaction ID is BDT90325114030699944. Visit MyGP to get attractive cashback on recharge https://mygp.li/sn",
    "You have Successfully recharged with amount 20.00 BDT.Transaction ID is BD090925183100069039. Visit MyGP to get attractive cashback on recharge https://mygp.li/sn",
    "You have Successfully recharged with amount 20.00 BDT.Transaction ID is BD071025164813113687. Visit MyGP to get attractive cashback on recharge https://mygp.li/sn",
    "You have Successfully recharged with amount 50.00 BDT.Transaction ID is BD091125201948063199. Visit MyGP to get attractive cashback on recharge https://mygp.li/sn",
    # Rokomari promotional messages
    "কোডে! মিস করবেন? ভিজিট- t.ly/lWxzl রকমারি",
    "আখেরি অফার বইয়ের ২৮% ছাড়, আর্পে ৮% এক্সট্রা ছাড় - t.ly/ohGLo রকমারি",
    "আজই শেষ হচ্ছে যে বিশেষ অফার!* বিস্তারিত জানতে- t.ly/3k3Al রকমারি।",
    "রকমারি ফ্রি বই ও ফ্রি পিপিং! আজ বিকেল ৩-৫ টা BUYDAY কোডে* - t.ly/PIRHI",
    ".com/WhTkt9CVS",
    "প্রোগ্রামিং শেখার বই অর্ডারে এক্সট্রা ২০% ছাড়! লিংক- rb.gy/agzprb",
    "নিশ্চিত উপহার,ফ্রি সিপিং,২৫% ছাড়*- 'ঈদি অফারে- rokshort.com/loK2eum3j",
    "৩০-৭০% ছাড় ১০% ক্যাশব্যাক রিয়েলেস সেল আজই শেষ* রকমারি - t.ly/ClN-v",
    "৭৭৭ টাকা বোনাস জিতেছে আপনি ইনস্টল করুন:https://cutt.ly/3rWpZ6xJ",
    # GovtInfo/Govt. Info messages
    "আজ ২৩ মে ২০২৪, বিশ্ব মেটেলিজি দিবস। এবারের প্রতিপাদ্য- 'টেকসই ভবিষ্যৎ বিনির্মাণে আজকের পরিমাপ', থিএসচিআই, শিল্প মন্ত্রণালয়।",
    '"অর্থনৈতিক শুমারি ২০২৪ এর আওতায় দেশের সকল খানা ও প্রতিষ্ঠান তালিকাভুক্ত করা হচ্ছ। জাতীয় স্বার্থপূর্ণ এ কার্যক্রমে আপনার তথ্য দিয়ে সহযোগিতা করুন" - বাংলাদেশ পরিসংখ্যান ব্যুরো।',
    '"সত্য নিয়ত্ম যাচাই আগে ইষ্টীরনেটে শেয়ার পরে" -ডাক টেলিযোগাযোগ ও তথ্য প্রযুক্তি প্রতিমন্ত্রী',
    "'পশ্চিন শান্তির সোপান।' আজ বিশ্ব পশ্চিন দিবস। নিরাপদ ও শান্তিপূর্ণ পশ্চিনের সাধ্যে টেকসই উন্নয়ন, সংস্কৃতি ও মূল্যবোধ প্রতিষ্ঠায় আমরা অঙ্গীকারাবদ্ধ। বেসামরিক বিমান পরিবহন ও পশ্চিন মন্ত্রণালয়।",
    '"জন্ম - মৃত্যু নিবন্ধন, আনবে দেশে সুশাসন"',
    "বাংলাদেশ পরিসংখ্যান ব্যুরো কর্তৃক প্রকাশিত সরকারের অগ্রগতি এবং উন্নয়নের চিত্রের গুরুত্বপূর্ণ প্রকাশনার লিংক- https://cutt.ly/0UjDTpk",
    "জুলাই 'পুনর্জাগরণ' অনুষ্ঠানমালার অংশ হিসেবে প্রস্তুতকৃত ভিডিও দেখতে https://www.youtube.com/@ministryofculturalaffairs8279/videos ভিজিট করুন। -সংস্কৃতি বিষয়ক মন্ত্রণালয়।",
    "অতিরিক্ত টিনি গ্রহণে মেদ বাহুল্য, ডায়াবেটিস, ক্যান্সার, ইদরোগ, ফ্যাটি লিভার, ক্যালার, ইনসুলিন প্রতিরোধ ইত্যাদি রোগের ঝুঁকি বেড়ে যায়। টিনি পরিমিত মাত্রায় গ্রহণ করুন, সুখ্যাস্থ্য বজায় রাখুন-বিএফএসএ",
    "বাংলাদেশ নৌবাহিনীতে অফিসার ক্যাডেট পদে নিয়োগ চলছে। ভিজিট করুন: http://joinnavy.navy.mil.bd",
    "ইভিএস এর প্রকৃত উদ্দেশ্য জাল ভোট বন্ধ করে জনগণের ভোটাধিকার সুনিশ্চিত করা-ইসি",
    '২২ সেপ্টেম্বর ২০২৯ "বিশ্ব ব্যক্তিগত গাড়িমুক্ত দিবস"। "গণপরিবহনে ও হেঁটে চলি, ব্যক্তিগত গাড়ি সীমিত করি"-ডিটিসিএ।',
    "বাংলাদেশ পরিসংখ্যান ব্যুরো কর্তৃক প্রকাশিত সরকারের অগ্রগতি এবং উন্নয়নের চিত্রের গুরুত্বপূর্ণ প্রকাশনার",
    # SHUKHEE promotional
    "shukhee Confirmation Code:9299 (Please do not share this code with anyone else)",
    "Shukhee এ আপনাকে স্বাগতম! আপনার আকাউন্টটি সফলভাবে তৈরি হয়েছে। আমাদের সাভিসগুলো উপভোগ করতে অথবা থেকোনো জরুরি প্রয়োজনে কল করুন, 10657",
    "জানুয়ারী মাসের উত্তৃষ্ট শেষ !! K3 ১৯% পর্ন্ত ছাড়ে আপনার ফেভারারী মাসের উত্তৃষ্ট অর্ডার করুন সূখীতে !! https://t.ly/8y4yY",
    "২০% পর্ন্ত ক্যাশব্যাক অফার !! সূখীর উর্ধ্ব কনসালটেশন সাভিস বিক্ষে পেতে পাবেন ইনস্ট্যান্ট ক্যাশব্যাক। https://shorturl.at/ipHBc",
    "সূখীতে ২০% ক্যাশব্যাক অফার !! সূখীর যে কোনো সাভিস বিক্ষে পেতে করবেন প্রতিদিন ৫০০ টাকা পর্ন্ত ক্যাশব্যাক। (সর্ব প্রথমে) https://shukhee.com/",
    "সূখী ভালোবাসা দিবসের অভেজ্ঞ !! ভালোবাটিস কাপল প্যাকেজে ৩৫% ছাড়! বিরেব আগে সব প্রয়োর উত্তর জানুন, তবে বিনোয়াসিন ইলেক্ট্রোমেক্সিন টেস্ট করাতে আর্ভ জরুরী! আজই বুক করুন বিশেষ ছাড়ে! https://shorturl.at/s1nB8",
    "বিবের আগে এই টেস্টা কিন করবেন না! বিনোয়াসিন ইলেক্ট্রোমেক্সিন টেস্ট করবেন আগে শারীরতে তরনার কোনো রক্তরোগ হবে কিনা? আজই বুক করুন ০৫% ছাড়ে! https://shorturl.at/yy1xY",
    # NewsUpdate
    "<<ব্রেকিং নিউজ>> কারাগার থেকে সেনানিবাসের সার্জেল ১৫ সেনা কর্মকর্তা..প্রতিদিন ১,৩৯ টাকা. এই ধরনের সর্বশেষ খবরগুলো পেতে http://wap.teletalk.com.bd/otp/request?redirectTo=user/aoc/news",
    # Additional bKashCS messages
    "Your Service Request Number is 8953. Please do not share it with anyone except bKash Customer Service Executive of bKash Grahok Sheba or livechat.bkash.com.",
    "Your Service Request Number is 6135. Please do not share it with anyone except bKash Customer Service Executive of bKash Grahok Sheba or livechat.bkash.com.",
    "শুধুমাত্র বিকাশ লাইভচ্যাট স্ক্রিনে সার্ভিস রিকোয়েস্ট নাম্বার 021065 লিখুন। কল বা SMS এর মাধ্যমে নাম্বারটি কারো সাথে শেয়ার করবেন না।",
    "শুধুমাত্র বিকাশ লাইভচ্যাট স্ক্রিনে সার্ভিস রিকোয়েস্ট নাম্বার 106248 লিখুন। কল বা SMS এর মাধ্যমে নাম্বারটি কারো সাথে শেয়ার করবেন না।",
    "শুধুমাত্র বিকাশ লাইভচ্যাট স্ক্রিনে সার্ভিস রিকোয়েস্ট নাম্বার 858961 লিখুন। কল বা SMS এর মাধ্যমে নাম্বারটি কারো সাথে শেয়ার করবেন না।",
    # JANATA BANK messages
    "Thank You.",
    "Your JBPLC. account *5877 credited with BDT 1000.00 from Medical College at 03 Jul 25 14:18:52 Balance is BDT 1040 . Enjoy Amar Sanchoy Amar Munafa",
    "Your JBPLC. account *5877 credited with BDT 1000.00 from Barisal Corporate at 06 Aug 25 13:39:33 Balance is BDT 1040 .",
    "Dear Sir, your JBPLC. A/C **5451 has been credited (Interest) by BDT2583.66 on 10-SEP-2025. C/B is BDT0. Use eJanata app for i-banking. Thanks",
    "Your JBPLC. account *5877 debited with BDT40.00 from Alinagar at 11 Sep 25 12:11:44 Balance is BDT 0 . Enjoy A-Challan from any branch",
    "Dear Sir, Your SMS Alert Mobile number has been changed from 01712911614 to 01721170869 at Janata Bank PLC. You will now receive SMS on the new number. Thank You.",
    "Your JBPLC. ATM Card No.7012***4920 debited with BDT20015.00. Balance is BDT14646.31. at 02 Dec 25 17:44:55 from Barishal ATM. Visit www.jb.com.bd for services",
    "40 . Enjoy JB Smart account",
    # EASYFASHION messages
    "ঈজি ফ্যাশনে নতুন ডিজাইনের ঈদ কালেকশন সকাল শাখায় tinyurl.com/5ejwmsxc",
    "ঈদ উপল আহয়া কালেকশন এখন ঈজি ফ্যাশনের সকল শাখায়। tinyurl.com/mzkj6a3x",
    "ঈজি ফ্যাশনের ঈদ উপহার নির্দিষ্ট পনু আকর্ষনীয় ছাড় tinyurl.com/4mtf8u3y",
    "শীতের নতুন কালেকশন এখন ঈজি ফ্যাশনের সকল শোরুমে। tinyurl.com/4jj6f5yu",
    # TrustBank messages
    "Balance TK 16992.14 Get email notification - t.tblbd.com/email",
    "প্রিয় গ্রাহক, ট্রাস্ট ব্যাংক কাষ্টমার সার্ভিস নাম্বার ১৬২০১ ব্যান্ত থাকলে ১৬৭৩৩ নাম্বারে কল করুন -ট্রাস্ট ব্যাংক।",
    "Your OTP is 708411. It will be valid for 3 minutes. Never share OTP, PIN, CVV, Expiry Date and Password with anyone. TBL-Digital Banking.",
    "TRUST MONEY Txn TK 50.00 DEBIT AC No 046***423 13/12/2025 04:04 Balance TK 18942.14 Get email notification - t.tblbd.com/email",
    # CITY_AMEX messages
    "আপনার আমেক্স ক্রেডিট কার্ড দিয়ে ২১ ডিসেম্বর ২০২৫-এর মধ্যে নূনতম ১০টি কেনাকাটা করে জিতুন ১,০০০ বোনাস মেম্বারশিপ রিওয়ার্ডস পয়েন্টস! শর্ত প্রযোজ্য। বিস্তারিত http://cbl.fyi/p4a",
    "আজই শেষ সুযোগ! জিতুন ১,০০০ বোনাস মেম্বারশিপ রিওয়ার্ডস পয়েন্টস নূনতম ১০টি কেনাকাটা করে ১৫-২১ নভেম্বর ২০২৫-এর মধ্যে আপনার আমেক্স ক্রেডিট কার্ড দিয়ে। শর্ত প্রযোজ্য। বিস্তারিত https://cbl.fyi/mr1",
    "foodpanda-তে ৫ ও ৬ ডিসেম্বর 'AMEX200' ব্যবহার করে উপভোগ করুন ২০০ টাকা পর্যন্ত সাশ্রয়। শর্ত প্রযোজ্য। বিস্তারিত www.cbl.fyi/f15",
    "৫,০০০ ডলার এনডোর্স করে উপভোগ করুন ৫,০০০ পর্যন্ত বোনাস এক্স আর পয়েন্টস ! বিস্তা: www.cbl.fyi/ec25",
    # bdtickets promotional
    "কল: ১৬৪৬০",
    "ভর্তি পরীক্ষার যাতায়াতের বাস টিকেট কাটতে ক্লিক: bdtickets.com কল ১৬৪৬০",
    "বাসের প্রতি টিকেটে ৮৫০ ছাড় কোড: 50TK0FF ক্লিক: bdtickets.com কল: ১৬৪৬০",
    "নিরাপদে বাড়ি ফিরুন, ঝামেলাহীন বাস টিকেট পেতে ক্লিক: bdtickets.com",
    # Teletalk call charges
    "সময় 00:00:12,কাটা হয়েছে 0.17 Taka,বর্তমান ব্যালেন্স 38.22 Taka",
    "সময় 00:00:37,কাটা হয়েছে 0.51 Taka,বর্তমান ব্যালেন্স 37.71 Taka",
    "সময় 00:00:33,কাটা হয়েছে 0.46 Taka,বর্তমান ব্যালেন্স 37.25 Taka",
    "সময় 00:00:36,কাটা হয়েছে 0.5 Taka,বর্তমান ব্যালেন্স 36.75 Taka",
    "সময় 00:00:13,কাটা হয়েছে 0.18 Taka,বর্তমান ব্যালেন্স 32.4 Taka",
    # EID offer message
    "এই ঈদে দুর্দান্ত অফার! ২০% ছাড়! বাট্টা স্টোরে শপুয়াত ১৭ই মে",
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
