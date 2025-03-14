import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
import os
import time
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Initialize bot with state storage
state_storage = StateMemoryStorage()
bot = telebot.TeleBot(TOKEN, state_storage=state_storage)

# Word database for different languages and levels
word_database = {
    'English': {
        'beginner': [
            {'word': 'Hello', 'meaning': 'مرحباً'},
            {'word': 'Thank you', 'meaning': 'شكراً لك'},
            {'word': 'Please', 'meaning': 'من فضلك'},
            {'word': 'Good morning', 'meaning': 'صباح الخير'},
            {'word': 'Goodbye', 'meaning': 'مع السلامة'},
            {'word': 'Welcome', 'meaning': 'أهلاً وسهلاً'},
            {'word': 'Sorry', 'meaning': 'آسف'},
            {'word': 'Yes', 'meaning': 'نعم'},
            {'word': 'No', 'meaning': 'لا'},
            {'word': 'Water', 'meaning': 'ماء'},
            {'word': 'Food', 'meaning': 'طعام'},
            {'word': 'Friend', 'meaning': 'صديق'}
        ],
        'intermediate': [
            {'word': 'Beautiful', 'meaning': 'جميل'},
            {'word': 'Experience', 'meaning': 'خبرة/تجربة'},
            {'word': 'Communication', 'meaning': 'تواصل'},
            {'word': 'Development', 'meaning': 'تطوير'},
            {'word': 'Important', 'meaning': 'مهم'},
            {'word': 'Achievement', 'meaning': 'إنجاز'},
            {'word': 'Challenge', 'meaning': 'تحدي'},
            {'word': 'Opportunity', 'meaning': 'فرصة'},
            {'word': 'Environment', 'meaning': 'بيئة'},
            {'word': 'Technology', 'meaning': 'تقنية'},
            {'word': 'Culture', 'meaning': 'ثقافة'},
            {'word': 'Society', 'meaning': 'مجتمع'}
        ],
        'advanced': [
            {'word': 'Sophisticated', 'meaning': 'متطور/راقي'},
            {'word': 'Entrepreneurship', 'meaning': 'ريادة الأعمال'},
            {'word': 'Philanthropy', 'meaning': 'العمل الخيري'},
            {'word': 'Consciousness', 'meaning': 'الوعي/الإدراك'},
            {'word': 'Extraordinary', 'meaning': 'استثنائي'},
            {'word': 'Sustainability', 'meaning': 'الاستدامة'},
            {'word': 'Innovation', 'meaning': 'الابتكار'},
            {'word': 'Phenomenon', 'meaning': 'ظاهرة'},
            {'word': 'Authenticity', 'meaning': 'أصالة'},
            {'word': 'Persistence', 'meaning': 'المثابرة'},
            {'word': 'Resilience', 'meaning': 'المرونة'},
            {'word': 'Integrity', 'meaning': 'النزاهة'}
        ]
    },
    'Spanish': {
        'beginner': [
            {'word': 'Hola', 'meaning': 'مرحباً'},
            {'word': 'Gracias', 'meaning': 'شكراً'},
            {'word': 'Por favor', 'meaning': 'من فضلك'},
            {'word': 'Buenos días', 'meaning': 'صباح الخير'},
            {'word': 'Adiós', 'meaning': 'مع السلامة'},
            {'word': 'Agua', 'meaning': 'ماء'},
            {'word': 'Pan', 'meaning': 'خبز'},
            {'word': 'Amigo', 'meaning': 'صديق'},
            {'word': 'Casa', 'meaning': 'منزل'},
            {'word': 'Familia', 'meaning': 'عائلة'},
            {'word': 'Nombre', 'meaning': 'اسم'},
            {'word': 'Bueno', 'meaning': 'جيد'}
        ],
        'intermediate': [
            {'word': 'Hermoso', 'meaning': 'جميل'},
            {'word': 'Experiencia', 'meaning': 'خبرة'},
            {'word': 'Comunicación', 'meaning': 'تواصل'},
            {'word': 'Desarrollo', 'meaning': 'تطوير'},
            {'word': 'Importante', 'meaning': 'مهم'},
            {'word': 'Trabajo', 'meaning': 'عمل'},
            {'word': 'Tiempo', 'meaning': 'وقت'},
            {'word': 'Cultura', 'meaning': 'ثقافة'},
            {'word': 'Viaje', 'meaning': 'سفر'},
            {'word': 'Educación', 'meaning': 'تعليم'},
            {'word': 'Música', 'meaning': 'موسيقى'},
            {'word': 'Tecnología', 'meaning': 'تقنية'}
        ],
        'advanced': [
            {'word': 'Sofisticado', 'meaning': 'متطور'},
            {'word': 'Emprendimiento', 'meaning': 'ريادة الأعمال'},
            {'word': 'Filantropía', 'meaning': 'العمل الخيري'},
            {'word': 'Conciencia', 'meaning': 'الوعي'},
            {'word': 'Extraordinario', 'meaning': 'استثنائي'},
            {'word': 'Sostenibilidad', 'meaning': 'الاستدامة'},
            {'word': 'Innovación', 'meaning': 'الابتكار'},
            {'word': 'Perseverancia', 'meaning': 'المثابرة'},
            {'word': 'Autenticidad', 'meaning': 'الأصالة'},
            {'word': 'Integridad', 'meaning': 'النزاهة'},
            {'word': 'Perspectiva', 'meaning': 'منظور'},
            {'word': 'Paradigma', 'meaning': 'نموذج'}
        ]
    },
    'Japanese': {
        'beginner': [
            {'word': 'こんにちは', 'meaning': 'مرحباً', 'furigana': 'konnichiwa'},
            {'word': 'ありがとう', 'meaning': 'شكراً', 'furigana': 'arigatou'},
            {'word': 'お願いします', 'meaning': 'من فضلك', 'furigana': 'onegaishimasu'},
            {'word': 'おはよう', 'meaning': 'صباح الخير', 'furigana': 'ohayou'},
            {'word': 'さようなら', 'meaning': 'مع السلامة', 'furigana': 'sayounara'},
            {'word': '水', 'meaning': 'ماء', 'furigana': 'mizu'},
            {'word': '食べ物', 'meaning': 'طعام', 'furigana': 'tabemono'},
            {'word': '友達', 'meaning': 'صديق', 'furigana': 'tomodachi'},
            {'word': '家', 'meaning': 'منزل', 'furigana': 'ie/uchi'},
            {'word': '家族', 'meaning': 'عائلة', 'furigana': 'kazoku'},
            {'word': '名前', 'meaning': 'اسم', 'furigana': 'namae'},
            {'word': '良い', 'meaning': 'جيد', 'furigana': 'yoi/ii'}
        ],
        'intermediate': [
            {'word': '美しい', 'meaning': 'جميل', 'furigana': 'utsukushii'},
            {'word': '経験', 'meaning': 'خبرة', 'furigana': 'keiken'},
            {'word': 'コミュニケーション', 'meaning': 'تواصل', 'furigana': 'komyunikeeshon'},
            {'word': '開発', 'meaning': 'تطوير', 'furigana': 'kaihatsu'},
            {'word': '重要', 'meaning': 'مهم', 'furigana': 'juuyou'},
            {'word': '仕事', 'meaning': 'عمل', 'furigana': 'shigoto'},
            {'word': '時間', 'meaning': 'وقت', 'furigana': 'jikan'},
            {'word': '文化', 'meaning': 'ثقافة', 'furigana': 'bunka'},
            {'word': '旅行', 'meaning': 'سفر', 'furigana': 'ryokou'},
            {'word': '教育', 'meaning': 'تعليم', 'furigana': 'kyouiku'},
            {'word': '音楽', 'meaning': 'موسيقى', 'furigana': 'ongaku'},
            {'word': '技術', 'meaning': 'تقنية', 'furigana': 'gijutsu'}
        ],
        'advanced': [
            {'word': '洗練された', 'meaning': 'متطور', 'furigana': 'senrensareta'},
            {'word': '起業家精神', 'meaning': 'ريادة الأعمال', 'furigana': 'kigyouka seishin'},
            {'word': '慈善事業', 'meaning': 'العمل الخيري', 'furigana': 'jizen jigyou'},
            {'word': '意識', 'meaning': 'الوعي', 'furigana': 'ishiki'},
            {'word': '素晴らしい', 'meaning': 'رائع', 'furigana': 'subarashii'},
            {'word': '持続可能性', 'meaning': 'الاستدامة', 'furigana': 'jizoku kanousei'},
            {'word': '革新', 'meaning': 'الابتكار', 'furigana': 'kakushin'},
            {'word': '現象', 'meaning': 'ظاهرة', 'furigana': 'genshou'},
            {'word': '本物', 'meaning': 'أصالة', 'furigana': 'honmono'},
            {'word': '忍耐', 'meaning': 'المثابرة', 'furigana': 'nintai'},
            {'word': '誠実さ', 'meaning': 'النزاهة', 'furigana': 'seijitsu-sa'},
            {'word': '展望', 'meaning': 'منظور', 'furigana': 'tenbou'}
        ]
    },
    'French': {
        'beginner': [
            {'word': 'Bonjour', 'meaning': 'مرحباً'},
            {'word': 'Merci', 'meaning': 'شكراً'},
            {'word': 'S\'il vous plaît', 'meaning': 'من فضلك'},
            {'word': 'Bon matin', 'meaning': 'صباح الخير'},
            {'word': 'Au revoir', 'meaning': 'مع السلامة'},
            {'word': 'Eau', 'meaning': 'ماء'},
            {'word': 'Pain', 'meaning': 'خبز'},
            {'word': 'Ami', 'meaning': 'صديق'},
            {'word': 'Maison', 'meaning': 'منزل'},
            {'word': 'Famille', 'meaning': 'عائلة'},
            {'word': 'Nom', 'meaning': 'اسم'},
            {'word': 'Bon', 'meaning': 'جيد'}
        ],
        'intermediate': [
            {'word': 'Beau', 'meaning': 'جميل'},
            {'word': 'Expérience', 'meaning': 'خبرة'},
            {'word': 'Communication', 'meaning': 'تواصل'},
            {'word': 'Développement', 'meaning': 'تطوير'},
            {'word': 'Important', 'meaning': 'مهم'},
            {'word': 'Travail', 'meaning': 'عمل'},
            {'word': 'Temps', 'meaning': 'وقت'},
            {'word': 'Culture', 'meaning': 'ثقافة'},
            {'word': 'Voyage', 'meaning': 'سفر'},
            {'word': 'Éducation', 'meaning': 'تعليم'},
            {'word': 'Musique', 'meaning': 'موسيقى'},
            {'word': 'Technologie', 'meaning': 'تقنية'}
        ],
        'advanced': [
            {'word': 'Sophistiqué', 'meaning': 'متطور'},
            {'word': 'Entrepreneuriat', 'meaning': 'ريادة الأعمال'},
            {'word': 'Philanthropie', 'meaning': 'العمل الخيري'},
            {'word': 'Conscience', 'meaning': 'الوعي'},
            {'word': 'Extraordinaire', 'meaning': 'استثنائي'},
            {'word': 'Durabilité', 'meaning': 'الاستدامة'},
            {'word': 'Innovation', 'meaning': 'الابتكار'},
            {'word': 'Phénomène', 'meaning': 'ظاهرة'},
            {'word': 'Authenticité', 'meaning': 'أصالة'},
            {'word': 'Persévérance', 'meaning': 'المثابرة'},
            {'word': 'Résilience', 'meaning': 'المرونة'},
            {'word': 'Intégrité', 'meaning': 'النزاهة'}
        ]
    },
    'Korean': {
        'beginner': [
            {'word': '안녕하세요', 'meaning': 'مرحباً'},
            {'word': '감사합니다', 'meaning': 'شكراً'},
            {'word': '주세요', 'meaning': 'من فضلك'},
            {'word': '좋은 아침', 'meaning': 'صباح الخير'},
            {'word': '안녕히 가세요', 'meaning': 'مع السلامة'},
            {'word': '물', 'meaning': 'ماء'},
            {'word': '음식', 'meaning': 'طعام'},
            {'word': '친구', 'meaning': 'صديق'},
            {'word': '집', 'meaning': 'منزل'},
            {'word': '가족', 'meaning': 'عائلة'},
            {'word': '이름', 'meaning': 'اسم'},
            {'word': '좋아요', 'meaning': 'جيد'}
        ],
        'intermediate': [
            {'word': '아름다운', 'meaning': 'جميل'},
            {'word': '경험', 'meaning': 'خبرة'},
            {'word': '의사소통', 'meaning': 'تواصل'},
            {'word': '발전', 'meaning': 'تطوير'},
            {'word': '중요한', 'meaning': 'مهم'},
            {'word': '일', 'meaning': 'عمل'},
            {'word': '시간', 'meaning': 'وقت'},
            {'word': '문화', 'meaning': 'ثقافة'},
            {'word': '여행', 'meaning': 'سفر'},
            {'word': '교육', 'meaning': 'تعليم'},
            {'word': '음악', 'meaning': 'موسيقى'},
            {'word': '기술', 'meaning': 'تقنية'}
        ],
        'advanced': [
            {'word': '세련된', 'meaning': 'متطور'},
            {'word': '기업가 정신', 'meaning': 'ريادة الأعمال'},
            {'word': '자선 사업', 'meaning': 'العمل الخيري'},
            {'word': '의식', 'meaning': 'الوعي'},
            {'word': '특별한', 'meaning': 'استثنائي'},
            {'word': '지속 가능성', 'meaning': 'الاستدامة'},
            {'word': '혁신', 'meaning': 'الابتكار'},
            {'word': '현상', 'meaning': 'ظاهرة'},
            {'word': '진정성', 'meaning': 'أصالة'},
            {'word': '인내', 'meaning': 'المثابرة'},
            {'word': '회복력', 'meaning': 'المرونة'},
            {'word': '성실성', 'meaning': 'النزاهة'}
        ]
    },
    'Russian': {
        'beginner': [
            {'word': 'Здравствуйте', 'meaning': 'مرحباً'},
            {'word': 'Спасибо', 'meaning': 'شكراً'},
            {'word': 'Пожалуйста', 'meaning': 'من فضلك'},
            {'word': 'Доброе утро', 'meaning': 'صباح الخير'},
            {'word': 'До свидания', 'meaning': 'مع السلامة'},
            {'word': 'Вода', 'meaning': 'ماء'},
            {'word': 'Еда', 'meaning': 'طعام'},
            {'word': 'Друг', 'meaning': 'صديق'},
            {'word': 'Дом', 'meaning': 'منزل'},
            {'word': 'Семья', 'meaning': 'عائلة'},
            {'word': 'Имя', 'meaning': 'اسم'},
            {'word': 'Хорошо', 'meaning': 'جيد'}
        ],
        'intermediate': [
            {'word': 'Красивый', 'meaning': 'جميل'},
            {'word': 'Опыт', 'meaning': 'خبرة'},
            {'word': 'Общение', 'meaning': 'تواصل'},
            {'word': 'Развитие', 'meaning': 'تطوير'},
            {'word': 'Важный', 'meaning': 'مهم'},
            {'word': 'Работа', 'meaning': 'عمل'},
            {'word': 'Время', 'meaning': 'وقت'},
            {'word': 'Культура', 'meaning': 'ثقافة'},
            {'word': 'Путешествие', 'meaning': 'سفر'},
            {'word': 'Образование', 'meaning': 'تعليم'},
            {'word': 'Музыка', 'meaning': 'موسيقى'},
            {'word': 'Технология', 'meaning': 'تقنية'}
        ],
        'advanced': [
            {'word': 'Утонченный', 'meaning': 'متطور'},
            {'word': 'Предпринимательство', 'meaning': 'ريادة الأعمال'},
            {'word': 'Филантропия', 'meaning': 'العمل الخيري'},
            {'word': 'Сознание', 'meaning': 'الوعي'},
            {'word': 'Необыкновенный', 'meaning': 'استثنائي'},
            {'word': 'Устойчивость', 'meaning': 'الاستدامة'},
            {'word': 'Инновация', 'meaning': 'الابتكار'},
            {'word': 'Феномен', 'meaning': 'ظاهرة'},
            {'word': 'Подлинность', 'meaning': 'أصالة'},
            {'word': 'Настойчивость', 'meaning': 'المثابرة'},
            {'word': 'Устойчивость', 'meaning': 'المرونة'},
            {'word': 'Целостность', 'meaning': 'النزاهة'}
        ]
    }
}

user_states = {}

def language_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*[KeyboardButton(lang) for lang in word_database.keys()])
    return keyboard

def level_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(
        KeyboardButton("مبتدئ"),
        KeyboardButton("متوسط"),
        KeyboardButton("متقدم")
    )
    return keyboard

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "مرحباً! اختر اللغة التي تباني اعطيك منها كلمة!:", reply_markup=language_keyboard())
    user_states[message.chat.id] = {'step': 'language_selection'}

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    if chat_id not in user_states:
        bot.reply_to(message, "الرجاء الضغط على /start للبدء")
        return

    if user_states[chat_id]['step'] == 'language_selection':
        if message.text in word_database:
            user_states[chat_id]['language'] = message.text
            user_states[chat_id]['step'] = 'level_selection'
            bot.reply_to(message, "اختر المستوى يا بطل/ة:", reply_markup=level_keyboard())
        else:
            bot.reply_to(message, "الرجاء اختيار لغة من القائمة", reply_markup=language_keyboard())

    elif user_states[chat_id]['step'] == 'level_selection':
        level_map = {'مبتدئ': 'beginner', 'متوسط': 'intermediate', 'متقدم': 'advanced'}
        if message.text in level_map:
            language = user_states[chat_id]['language']
            level = level_map[message.text]
            import random
            word_data = random.choice(word_database[language][level])
            
            # تعديل طريقة عرض الكلمات اليابانية لتشمل الفوريغانا
            if language == 'Japanese':
                bot.reply_to(message, 
                    f"كلمة اليوم في اللغة {language} (مستوى {message.text}):\n\n"
                    f"الكلمة: {word_data['word']}\n"
                    f"النطق: {word_data['furigana']}\n"
                    f"المعنى: {word_data['meaning']}"
                )
            else:
                bot.reply_to(message, 
                    f"كلمة اليوم في اللغة {language} (مستوى {message.text}):\n\n"
                    f"الكلمة: {word_data['word']}\n"
                    f"المعنى: {word_data['meaning']}"
                )
                
            user_states[chat_id]['step'] = 'language_selection'
            bot.reply_to(message, "اختر لغة أخرى للكلمة الجاية:", reply_markup=language_keyboard())
        else:
            bot.reply_to(message, "الرجاء اختيار مستوى من القائمة", reply_markup=level_keyboard())

if __name__ == "__main__":
    while True:
        try:
            print("Bot is starting...")
            bot.remove_webhook()
            time.sleep(1)  # Give some time between removing webhook and polling
            bot.infinity_polling(timeout=60, long_polling_timeout=60)
        except Exception as e:
            print(f"Bot encountered an error: {e}")
            time.sleep(3)  # Wait before trying to reconnect
            continue
