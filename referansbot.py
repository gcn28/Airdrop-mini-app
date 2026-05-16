import sqlite3
import random
import time
import threading
import os
from datetime import datetime
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8784949212:AAHvIdGgPzmzsaTuO22RF8N6yUuuUuXx0ls"
ADMIN_ID = 8482383833
CHANNEL1 = "@cryptoxd_ru"
CHANNEL2 = "@mutualrefchannel"
REQUIRED_CHANNELS = [CHANNEL1, CHANNEL2]
BOT_USERNAME = "mutualref_bot"

bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

DB_PATH = "bot_database.db"

# ================= 7 DİL DESTEĞİ =================
t = {
    'tr': {
        'select_lang': "🌍 Dil seçin:",
        'join': "📢 KANALA KATIL:",
        'check': "✅ KATILDIM",
        'not_member': "❌ Önce kanala katıl!",
        'welcome': "🚀 HOŞ GELDİN!\n\n📌 Referans linkini gönder.\n🔄 Sistem seni eşleştirir.\n🎁 Her görevde +1 puan.\n⚠️ Günlük 40 görev.",
        'ref_btn': "🎯 Referans Linkim",
        'points_btn': "💎 Puanlarım",
        'admin_btn': "✉️ Admin Mesaj",
        'stats_btn': "📊 İstatistik",
        'admin_panel_btn': "👑 Admin Panel",
        'send_link': "📤 Referans linkini gönder:",
        'limit': "❌ 40 görev limitin doldu!",
        'my_link': "🔗 Linkin: {link}\n\n💎 Puan: {points}\n📊 Bugün: {tasks}/40",
        'change': "🔄 Link Değiştir",
        'exit': "🚪 Sıradan Çık",
        'join_q': "🚪 Sıraya Gir",
        'changed': "✅ Link değişti. Yeni link gönder:",
        'exited': "✅ Sıradan çıktın.",
        'joined': "✅ Sıraya girdin. Eşleşme aranıyor...",
        'fast_q': "⚡ 5 puan ile hızlı eşleşme?",
        'pay5': "💎 5 Puan Öde",
        'normal': "⏳ Normal Sıra",
        'no_points': "❌ 5 puanın yok! Puanın: {points}",
        'priority_ok': "✅ Öncelikli sıradasın!",
        'saved_ok': "✅ Link kaydedildi.",
        'match_msg': "🔗 EŞLEŞME BULUNDU!\n\n📌 Görev No: #{code}\n\n🤝 KARŞI TARAFIN LİNKİ:\n{link}\n\n⬆️ Linke TIKLA, botu başlat, sonra ✅ KAYIT OLDUM butonuna bas.",
        'done_btn': "✅ Kayıt Oldum",
        'already_btn': "⚠️ Önceden Başlatmışım",
        'confirm_msg': "📌 Görev #{code}\n\n✅ Kullanıcı kayıt olduğunu söylüyor.\n<b>ONAYLIYOR MUSUN?</b>",
        'yes_btn': "✅ Evet, Onaylıyorum",
        'retry_btn': "🔁 Tekrar Yapmasını Rica Et",
        'complete_msg': "✅ GÖREV TAMAMLANDI! +1 puan!\n📌 Görev No: #{code}\n📊 Bugün: {tasks}/40",
        'retry_msg': "❌ Kayıt olmadığını söylüyor. Linke tıkla ve botu başlat!",
        'new_link_req': "📤 Kullanıcı botu önceden başlattığını söyledi.\n📌 Görev No: #{code}\n\n<b>YENİ BİR REFERANS LİNKİ GÖNDER:</b>\nBu link KARŞI TARAFA iletilecektir.",
        'new_link_ok': "✅ TELAFİ LİNKİ ALINDI!\n📌 Görev No: #{code}\n\n🤝 SANA GÖNDERİLEN TELAFİ LİNKİ:\n{link}\n\n⬆️ Linke TIKLA, botu başlat, sonra ✅ KAYIT OLDUM butonuna bas.",
        'points_info': "💎 Puanın: {points}\n\n🔗 Referans linkin: {link}",
        'admin_prompt': "📝 Mesajını yaz:",
        'admin_sent': "✅ İletildi.",
        'stats': "📊 İSTATİSTİK\n👥 Kullanıcı: {users}\n✅ Görev: {tasks}",
        'admin_welcome': "👑 ADMIN PANELİ",
        'broadcast_btn': "📢 Duyuru",
        'private_btn': "👤 Özel Mesaj",
        'back_btn': "🔙 Ana Menü",
        'broadcast_prompt': "📢 Duyuru mesajını yaz:",
        'invalid_link': "❌ Geçersiz link!",
        'need_link': "❌ Önce link gönder!",
        'enter_id': "👤 ID yaz:",
        'enter_msg': "💬 Mesaj yaz:",
        'invalid_id': "❌ Geçersiz ID!",
        'private_ok': "✅ Gönderildi.",
        'private_fail': "❌ Gönderilemedi!",
        'broadcast_ok': "✅ Duyuru bitti!\n✅ {ok} başarılı\n❌ {fail} başarısız",
        'new_msg': "📩 YENİ MESAJ\n👤 {uid}\n💬 {msg}",
        'already_today': "❌ Bugün zaten gönderdin!",
        'done_sent': "✅ 'Kayıt Oldum' bildirimi karşı tarafa iletildi!",
        'confirm_sent': "✅ Onayın karşı tarafa iletildi!",
        'already_sent': "✅ Bilgi iletildi! Karşı taraftan yeni link bekleniyor.",
        'waiting_both': "⏳ Her iki tarafın da onayı bekleniyor...",
        'waiting_other': "⏳ Karşı tarafın onayı bekleniyor...",
        'both_confirmed': "✅ İKİ TARAF DA ONAYLADI! Görev tamamlandı!"
    },
    'ru': {
        'select_lang': "🌍 Выберите язык:",
        'join': "📢 ПОДПИШИСЬ:",
        'check': "✅ ПОДПИСАЛСЯ",
        'not_member': "❌ Подпишись сначала!",
        'welcome': "🚀 ДОБРО ПОЖАЛОВАТЬ!\n\n📌 Отправь ссылку.\n🔄 Найду пару.\n🎁 +1 балл.\n⚠️ 40 заданий в день.",
        'ref_btn': "🎯 Моя ссылка",
        'points_btn': "💎 Мои баллы",
        'admin_btn': "✉️ Админу",
        'stats_btn': "📊 Статистика",
        'admin_panel_btn': "👑 Админ панель",
        'send_link': "📤 Отправь ссылку:",
        'limit': "❌ 40 заданий на сегодня!",
        'my_link': "🔗 Твоя ссылка: {link}\n\n💎 Баллы: {points}\n📊 Сегодня: {tasks}/40",
        'change': "🔄 Изменить",
        'exit': "🚪 Выйти",
        'join_q': "🚪 Войти",
        'changed': "✅ Ссылка изменена.",
        'exited': "✅ Вышел.",
        'joined': "✅ В очереди. Ищу пару...",
        'fast_q': "⚡ Быстрый поиск за 5 баллов?",
        'pay5': "💎 5 баллов",
        'normal': "⏳ Обычная очередь",
        'no_points': "❌ Нужно 5 баллов! У тебя: {points}",
        'priority_ok': "✅ Ты в приоритете!",
        'saved_ok': "✅ Ссылка сохранена.",
        'match_msg': "🔗 ПАРА НАЙДЕНА!\n\n📌 Задание №: #{code}\n\n🤝 Ссылка другого:\n{link}\n\n⬆️ Нажми, запусти бота, затем ✅ ЗАРЕГИСТРИРОВАЛСЯ.",
        'done_btn': "✅ Зарегился",
        'already_btn': "⚠️ Уже запускал",
        'confirm_msg': "📌 Задание #{code}\n\n✅ Пользователь подтверждает. Подтверждаешь?",
        'yes_btn': "✅ Да",
        'retry_btn': "🔁 Повторить",
        'complete_msg': "✅ ЗАДАНИЕ ВЫПОЛНЕНО! +1 балл! #{code}\n📊 Сегодня: {tasks}/40",
        'retry_msg': "❌ Говорит, что ты не зарегился. Нажми на ссылку и запусти бота!",
        'new_link_req': "📤 Пользователь уже запускал бота.\n📌 Задание №: #{code}\n\n<b>ОТПРАВЬ НОВУЮ ССЫЛКУ:</b>\nЭта ссылка будет отправлена другой стороне.",
        'new_link_ok': "✅ КОМПЕНСАЦИОННАЯ ССЫЛКА ПОЛУЧЕНА!\n📌 Задание №: #{code}\n\n🤝 КОМПЕНСАЦИОННАЯ ССЫЛКА ДЛЯ ТЕБЯ:\n{link}\n\n⬆️ Нажми, запусти бота, затем ✅ ЗАРЕГИСТРИРОВАЛСЯ.",
        'points_info': "💎 Баллы: {points}\n\n🔗 Твоя ссылка: {link}",
        'admin_prompt': "📝 Напиши сообщение:",
        'admin_sent': "✅ Отправлено.",
        'stats': "📊 СТАТИСТИКА\n👥 Пользователей: {users}\n✅ Заданий: {tasks}",
        'admin_welcome': "👑 АДМИН ПАНЕЛЬ",
        'broadcast_btn': "📢 Всем",
        'private_btn': "👤 Пользователю",
        'back_btn': "🔙 Главное меню",
        'broadcast_prompt': "📢 Напиши объявление:",
        'invalid_link': "❌ Неверная ссылка!",
        'need_link': "❌ Сначала отправь ссылку!",
        'enter_id': "👤 Введи ID:",
        'enter_msg': "💬 Введи сообщение:",
        'invalid_id': "❌ Неверный ID!",
        'private_ok': "✅ Отправлено.",
        'private_fail': "❌ Не отправлено!",
        'broadcast_ok': "✅ Готово!\n✅ {ok} успешно\n❌ {fail} ошибок",
        'new_msg': "📩 НОВОЕ СООБЩЕНИЕ\n👤 {uid}\n💬 {msg}",
        'already_today': "❌ Сегодня уже отправлял!",
        'done_sent': "✅ 'Зарегился' отправлено другой стороне!",
        'confirm_sent': "✅ Подтверждение отправлено!",
        'already_sent': "✅ Информация отправлена! Ожидание новой ссылки.",
        'waiting_both': "⏳ Ожидание подтверждения от обеих сторон...",
        'waiting_other': "⏳ Ожидание подтверждения от другой стороны...",
        'both_confirmed': "✅ ОБЕ СТОРОНЫ ПОДТВЕРДИЛИ! Задание выполнено!"
    },
    'en': {
        'select_lang': "🌍 Choose language:",
        'join': "📢 JOIN CHANNEL:",
        'check': "✅ JOINED",
        'not_member': "❌ Join channel first!",
        'welcome': "🚀 WELCOME!\n\n📌 Send your referral link.\n🔄 Get matched.\n🎁 +1 point.\n⚠️ 40 tasks daily.",
        'ref_btn': "🎯 My Referral Link",
        'points_btn': "💎 My Points",
        'admin_btn': "✉️ Message Admin",
        'stats_btn': "📊 Statistics",
        'admin_panel_btn': "👑 Admin Panel",
        'send_link': "📤 Send your referral link:",
        'limit': "❌ Daily limit 40 reached!",
        'my_link': "🔗 Your link: {link}\n\n💎 Points: {points}\n📊 Today: {tasks}/40",
        'change': "🔄 Change Link",
        'exit': "🚪 Exit Queue",
        'join_q': "🚪 Join Queue",
        'changed': "✅ Link changed.",
        'exited': "✅ Exited queue.",
        'joined': "✅ Joined queue. Looking for match...",
        'fast_q': "⚡ Fast match for 5 points?",
        'pay5': "💎 Pay 5 Points",
        'normal': "⏳ Normal Queue",
        'no_points': "❌ Need 5 points! You have: {points}",
        'priority_ok': "✅ You're in priority queue!",
        'saved_ok': "✅ Link saved.",
        'match_msg': "🔗 MATCH FOUND!\n\n📌 Task No: #{code}\n\n🤝 Other user's link:\n{link}\n\n⬆️ Click, start the bot, then ✅ REGISTERED.",
        'done_btn': "✅ Registered",
        'already_btn': "⚠️ Already Started",
        'confirm_msg': "📌 Task #{code}\n\n✅ User confirms registration. Confirm?",
        'yes_btn': "✅ Yes",
        'retry_btn': "🔁 Ask to Retry",
        'complete_msg': "✅ TASK COMPLETED! +1 point! #{code}\n📊 Today: {tasks}/40",
        'retry_msg': "❌ User says you didn't register. Click the link and start the bot!",
        'new_link_req': "📤 User already started the bot.\n📌 Task No: #{code}\n\n<b>SEND A NEW REFERRAL LINK:</b>\nThis link will be sent to the other party.",
        'new_link_ok': "✅ COMPENSATION LINK RECEIVED!\n📌 Task No: #{code}\n\n🤝 COMPENSATION LINK FOR YOU:\n{link}\n\n⬆️ Click, start the bot, then ✅ REGISTERED.",
        'points_info': "💎 Your points: {points}\n\n🔗 Your referral link: {link}",
        'admin_prompt': "📝 Write your message:",
        'admin_sent': "✅ Sent.",
        'stats': "📊 STATISTICS\n👥 Users: {users}\n✅ Tasks: {tasks}",
        'admin_welcome': "👑 ADMIN PANEL",
        'broadcast_btn': "📢 Broadcast",
        'private_btn': "👤 Private Message",
        'back_btn': "🔙 Main Menu",
        'broadcast_prompt': "📢 Write announcement:",
        'invalid_link': "❌ Invalid link!",
        'need_link': "❌ Send a link first!",
        'enter_id': "👤 Enter user ID:",
        'enter_msg': "💬 Enter message:",
        'invalid_id': "❌ Invalid ID!",
        'private_ok': "✅ Sent.",
        'private_fail': "❌ Failed to send!",
        'broadcast_ok': "✅ Done!\n✅ Success: {ok}\n❌ Failed: {fail}",
        'new_msg': "📩 NEW MESSAGE\n👤 {uid}\n💬 {msg}",
        'already_today': "❌ Already sent today!",
        'done_sent': "✅ 'Registered' sent to the other party!",
        'confirm_sent': "✅ Confirmation sent!",
        'already_sent': "✅ Info sent! Waiting for new link from other party.",
        'waiting_both': "⏳ Waiting for both parties to confirm...",
        'waiting_other': "⏳ Waiting for other party's confirmation...",
        'both_confirmed': "✅ BOTH PARTIES CONFIRMED! Task completed!"
    },
    'de': {
        'select_lang': "🌍 Wähle eine Sprache:",
        'join': "📢 TRITT DEM KANAL BEI:",
        'check': "✅ BEIGETRETEN",
        'not_member': "❌ Tritt zuerst dem Kanal bei!",
        'welcome': "🚀 WILLKOMMEN!\n\n📌 Sende deinen Link.\n🔄 Finde einen Partner.\n🎁 +1 Punkt.\n⚠️ 40 Aufgaben täglich.",
        'ref_btn': "🎯 Mein Link",
        'points_btn': "💎 Meine Punkte",
        'admin_btn': "✉️ Admin",
        'stats_btn': "📊 Statistik",
        'admin_panel_btn': "👑 Admin Panel",
        'send_link': "📤 Sende deinen Link:",
        'limit': "❌ 40 Aufgaben Limit erreicht!",
        'my_link': "🔗 Dein Link: {link}\n\n💎 Punkte: {points}\n📊 Heute: {tasks}/40",
        'change': "🔄 Link ändern",
        'exit': "🚪 Warteschlange verlassen",
        'join_q': "🚪 Beitreten",
        'changed': "✅ Link geändert.",
        'exited': "✅ Ausgetreten.",
        'joined': "✅ In der Warteschlange. Suche Partner...",
        'fast_q': "⚡ Schnelles Matching für 5 Punkte?",
        'pay5': "💎 5 Punkte zahlen",
        'normal': "⏳ Normale Warteschlange",
        'no_points': "❌ Brauche 5 Punkte! Du hast: {points}",
        'priority_ok': "✅ Du bist in der Prioritätswarteschlange!",
        'saved_ok': "✅ Link gespeichert.",
        'match_msg': "🔗 PARTNER GEFUNDEN!\n\n📌 Aufgabe Nr: #{code}\n\n🤝 Link des anderen:\n{link}\n\n⬆️ Klicke, starte den Bot, dann ✅ REGISTRIERT.",
        'done_btn': "✅ Registriert",
        'already_btn': "⚠️ Schon gestartet",
        'confirm_msg': "📌 Aufgabe #{code}\n\n✅ Benutzer bestätigt. Bestätigst du?",
        'yes_btn': "✅ Ja",
        'retry_btn': "🔁 Wiederholen",
        'complete_msg': "✅ AUFGABE ABGESCHLOSSEN! +1 Punkt! #{code}\n📊 Heute: {tasks}/40",
        'retry_msg': "❌ Benutzer sagt, du bist nicht registriert. Klicke den Link und starte den Bot!",
        'new_link_req': "📤 Benutzer hat den Bot schon gestartet.\n📌 Aufgabe Nr: #{code}\n\n<b>SENDE EINEN NEUEN LINK:</b>\nDieser Link wird an die andere Seite gesendet.",
        'new_link_ok': "✅ AUSGLEICHSLINK ERHALTEN!\n📌 Aufgabe Nr: #{code}\n\n🤝 AUSGLEICHSLINK FÜR DICH:\n{link}\n\n⬆️ Klicke, starte den Bot, dann ✅ REGISTRIERT.",
        'points_info': "💎 Deine Punkte: {points}\n\n🔗 Dein Link: {link}",
        'admin_prompt': "📝 Schreibe deine Nachricht:",
        'admin_sent': "✅ Gesendet.",
        'stats': "📊 STATISTIK\n👥 Benutzer: {users}\n✅ Aufgaben: {tasks}",
        'admin_welcome': "👑 ADMIN PANEL",
        'broadcast_btn': "📢 An alle",
        'private_btn': "👤 Private Nachricht",
        'back_btn': "🔙 Hauptmenü",
        'broadcast_prompt': "📢 Schreibe die Ankündigung:",
        'invalid_link': "❌ Ungültiger Link!",
        'need_link': "❌ Sende zuerst einen Link!",
        'enter_id': "👤 Benutzer-ID:",
        'enter_msg': "💬 Nachricht:",
        'invalid_id': "❌ Ungültige ID!",
        'private_ok': "✅ Gesendet.",
        'private_fail': "❌ Fehlgeschlagen!",
        'broadcast_ok': "✅ Fertig!\n✅ Erfolg: {ok}\n❌ Fehler: {fail}",
        'new_msg': "📩 NEUE NACHRICHT\n👤 {uid}\n💬 {msg}",
        'already_today': "❌ Heute schon gesendet!",
        'done_sent': "✅ 'Registriert' an andere Seite gesendet!",
        'confirm_sent': "✅ Bestätigung gesendet!",
        'already_sent': "✅ Info gesendet! Warte auf neuen Link.",
        'waiting_both': "⏳ Warte auf Bestätigung beider Seiten...",
        'waiting_other': "⏳ Warte auf Bestätigung der anderen Seite...",
        'both_confirmed': "✅ BEIDE SEITEN BESTÄTIGT! Aufgabe abgeschlossen!"
    },
    'fr': {
        'select_lang': "🌍 Choisis une langue:",
        'join': "📢 REJOINS LE CANAL:",
        'check': "✅ REJOINT",
        'not_member': "❌ Rejoins d'abord le canal!",
        'welcome': "🚀 BIENVENUE!\n\n📌 Envoie ton lien.\n🔄 Trouve un partenaire.\n🎁 +1 point.\n⚠️ 40 tâches par jour.",
        'ref_btn': "🎯 Mon lien",
        'points_btn': "💎 Mes points",
        'admin_btn': "✉️ Admin",
        'stats_btn': "📊 Statistiques",
        'admin_panel_btn': "👑 Panneau admin",
        'send_link': "📤 Envoie ton lien:",
        'limit': "❌ Limite de 40 tâches atteinte!",
        'my_link': "🔗 Ton lien: {link}\n\n💎 Points: {points}\n📊 Aujourd'hui: {tasks}/40",
        'change': "🔄 Changer le lien",
        'exit': "🚪 Quitter la file",
        'join_q': "🚪 Rejoindre",
        'changed': "✅ Lien changé.",
        'exited': "✅ Quitté.",
        'joined': "✅ Dans la file. Recherche...",
        'fast_q': "⚡ Match rapide pour 5 points?",
        'pay5': "💎 Payer 5 points",
        'normal': "⏳ File normale",
        'no_points': "❌ Besoin de 5 points! Tu as: {points}",
        'priority_ok': "✅ File prioritaire!",
        'saved_ok': "✅ Lien sauvegardé.",
        'match_msg': "🔗 PARTENAIRE TROUVÉ!\n\n📌 Tâche No: #{code}\n\n🤝 Lien de l'autre:\n{link}\n\n⬆️ Clique, lance le bot, puis ✅ ENREGISTRÉ.",
        'done_btn': "✅ Enregistré",
        'already_btn': "⚠️ Déjà lancé",
        'confirm_msg': "📌 Tâche #{code}\n\n✅ L'utilisateur confirme. Tu confirmes?",
        'yes_btn': "✅ Oui",
        'retry_btn': "🔁 Réessayer",
        'complete_msg': "✅ TÂCHE TERMINÉE! +1 point! #{code}\n📊 Aujourd'hui: {tasks}/40",
        'retry_msg': "❌ L'utilisateur dit que tu ne t'es pas enregistré. Clique sur le lien et lance le bot!",
        'new_link_req': "📤 L'utilisateur a déjà lancé le bot.\n📌 Tâche No: #{code}\n\n<b>ENVOIE UN NOUVEAU LIEN:</b>\nCe lien sera envoyé à l'autre partie.",
        'new_link_ok': "✅ LIEN DE COMPENSATION REÇU!\n📌 Tâche No: #{code}\n\n🤝 LIEN DE COMPENSATION POUR TOI:\n{link}\n\n⬆️ Clique, lance le bot, puis ✅ ENREGISTRÉ.",
        'points_info': "💎 Tes points: {points}\n\n🔗 Ton lien: {link}",
        'admin_prompt': "📝 Écris ton message:",
        'admin_sent': "✅ Envoyé.",
        'stats': "📊 STATISTIQUES\n👥 Utilisateurs: {users}\n✅ Tâches: {tasks}",
        'admin_welcome': "👑 PANNELLO ADMIN",
        'broadcast_btn': "📢 Diffusion",
        'private_btn': "👤 Message privé",
        'back_btn': "🔙 Menu principal",
        'broadcast_prompt': "📢 Écris l'annonce:",
        'invalid_link': "❌ Lien invalide!",
        'need_link': "❌ Envoie d'abord un lien!",
        'enter_id': "👤 ID utilisateur:",
        'enter_msg': "💬 Message:",
        'invalid_id': "❌ ID invalide!",
        'private_ok': "✅ Envoyé.",
        'private_fail': "❌ Échec!",
        'broadcast_ok': "✅ Terminé!\n✅ Succès: {ok}\n❌ Échecs: {fail}",
        'new_msg': "📩 NOUVEAU MESSAGE\n👤 {uid}\n💬 {msg}",
        'already_today': "❌ Déjà envoyé aujourd'hui!",
        'done_sent': "✅ 'Enregistré' envoyé à l'autre partie!",
        'confirm_sent': "✅ Confirmation envoyée!",
        'already_sent': "✅ Info envoyée! Attente nouveau lien.",
        'waiting_both': "⏳ Attente confirmation des deux côtés...",
        'waiting_other': "⏳ Attente confirmation de l'autre côté...",
        'both_confirmed': "✅ LES DEUX CÔTÉS ONT CONFIRMÉ! Tâche terminée!"
    },
    'es': {
        'select_lang': "🌍 Elige un idioma:",
        'join': "📢 ÚNETE AL CANAL:",
        'check': "✅ ME UNÍ",
        'not_member': "❌ ¡Únete al canal primero!",
        'welcome': "🚀 ¡BIENVENIDO!\n\n📌 Envía tu enlace de referencia.\n🔄 Sistema te emparejará.\n🎁 +1 punto por tarea.\n⚠️ 40 tareas diarias.",
        'ref_btn': "🎯 Mi Enlace de Referencia",
        'points_btn': "💎 Mis Puntos",
        'admin_btn': "✉️ Mensaje al Admin",
        'stats_btn': "📊 Estadísticas",
        'admin_panel_btn': "👑 Panel de Admin",
        'send_link': "📤 Envía tu enlace de referencia:",
        'limit': "❌ ¡Límite de 40 tareas alcanzado!",
        'my_link': "🔗 Tu enlace: {link}\n\n💎 Puntos: {points}\n📊 Hoy: {tasks}/40",
        'change': "🔄 Cambiar Enlace",
        'exit': "🚪 Salir de la Cola",
        'join_q': "🚪 Unirse a la Cola",
        'changed': "✅ Enlace cambiado. Envía nuevo enlace:",
        'exited': "✅ Saliste de la cola.",
        'joined': "✅ En la cola. Buscando pareja...",
        'fast_q': "⚡ ¿Emparejamiento rápido por 5 puntos?",
        'pay5': "💎 Pagar 5 Puntos",
        'normal': "⏳ Cola Normal",
        'no_points': "❌ ¡Necesitas 5 puntos! Tienes: {points}",
        'priority_ok': "✅ ¡Estás en cola prioritaria!",
        'saved_ok': "✅ Enlace guardado.",
        'match_msg': "🔗 ¡PAREJA ENCONTRADA!\n\n📌 Tarea No: #{code}\n\n🤝 Enlace del otro usuario:\n{link}\n\n⬆️ Haz clic, inicia el bot, luego ✅ REGISTRADO.",
        'done_btn': "✅ Registrado",
        'already_btn': "⚠️ Ya Iniciado",
        'confirm_msg': "📌 Tarea #{code}\n\n✅ El usuario confirma el registro. ¿Confirmas?",
        'yes_btn': "✅ Sí",
        'retry_btn': "🔁 Pedir Reintentar",
        'complete_msg': "✅ ¡TAREA COMPLETADA! +1 punto! #{code}\n📊 Hoy: {tasks}/40",
        'retry_msg': "❌ El usuario dice que no te registraste. ¡Haz clic en el enlace e inicia el bot!",
        'new_link_req': "📤 El usuario ya inició el bot.\n📌 Tarea No: #{code}\n\n<b>ENVÍA UN NUEVO ENLACE DE REFERENCIA:</b>\nEste enlace se enviará a la otra parte.",
        'new_link_ok': "✅ ¡ENLACE DE COMPENSACIÓN RECIBIDO!\n📌 Tarea No: #{code}\n\n🤝 ENLACE DE COMPENSACIÓN PARA TI:\n{link}\n\n⬆️ Haz clic, inicia el bot, luego ✅ REGISTRADO.",
        'points_info': "💎 Tus puntos: {points}\n\n🔗 Tu enlace de referencia: {link}",
        'admin_prompt': "📝 Escribe tu mensaje:",
        'admin_sent': "✅ Enviado.",
        'stats': "📊 ESTADÍSTICAS\n👥 Usuarios: {users}\n✅ Tareas: {tasks}",
        'admin_welcome': "👑 PANEL DE ADMIN",
        'broadcast_btn': "📢 Transmitir",
        'private_btn': "👤 Mensaje Privado",
        'back_btn': "🔙 Menú Principal",
        'broadcast_prompt': "📢 Escribe el anuncio:",
        'invalid_link': "❌ ¡Enlace inválido!",
        'need_link': "❌ ¡Envía un enlace primero!",
        'enter_id': "👤 Escribe el ID:",
        'enter_msg': "💬 Escribe el mensaje:",
        'invalid_id': "❌ ¡ID inválido!",
        'private_ok': "✅ Enviado.",
        'private_fail': "❌ ¡Error al enviar!",
        'broadcast_ok': "✅ ¡Transmisión completada!\n✅ Éxito: {ok}\n❌ Fallos: {fail}",
        'new_msg': "📩 NUEVO MENSAJE\n👤 {uid}\n💬 {msg}",
        'already_today': "❌ ¡Ya enviaste hoy!",
        'done_sent': "✅ ¡Notificación 'Registrado' enviada a la otra parte!",
        'confirm_sent': "✅ ¡Confirmación enviada!",
        'already_sent': "✅ ¡Info enviada! Esperando nuevo enlace.",
        'waiting_both': "⏳ Esperando confirmación de ambas partes...",
        'waiting_other': "⏳ Esperando confirmación de la otra parte...",
        'both_confirmed': "✅ ¡AMBAS PARTES CONFIRMARON! Tarea completada!"
    },
    'ar': {
        'select_lang': "🌍 اختر اللغة:",
        'join': "📢 انضم إلى القناة:",
        'check': "✅ انضممت",
        'not_member': "❌ انضم إلى القناة أولاً!",
        'welcome': "🚀 مرحبا بك!\n\n📌 أرسل رابط الإحالة الخاص بك.\n🔄 سيقوم النظام بمطابقتك.\n🎁 +1 نقطة لكل مهمة.\n⚠️ 40 مهمة يومياً.",
        'ref_btn': "🎯 رابط الإحالة الخاص بي",
        'points_btn': "💎 نقاطي",
        'admin_btn': "✉️ أرسل إلى المدير",
        'stats_btn': "📊 إحصائيات",
        'admin_panel_btn': "👑 لوحة المدير",
        'send_link': "📤 أرسل رابط الإحالة:",
        'limit': "❌ تم الوصول إلى الحد اليومي 40!",
        'my_link': "🔗 رابطك: {link}\n\n💎 النقاط: {points}\n📊 اليوم: {tasks}/40",
        'change': "🔄 تغيير الرابط",
        'exit': "🚪 الخروج من قائمة الانتظار",
        'join_q': "🚪 الانضمام إلى قائمة الانتظار",
        'changed': "✅ تم تغيير الرابط. أرسل رابطاً جديداً:",
        'exited': "✅ خرجت من قائمة الانتظار.",
        'joined': "✅ انضممت إلى قائمة الانتظار. جاري البحث...",
        'fast_q': "⚡ مطابقة سريعة مقابل 5 نقاط؟",
        'pay5': "💎 دفع 5 نقاط",
        'normal': "⏳ قائمة عادية",
        'no_points': "❌ تحتاج 5 نقاط! لديك: {points}",
        'priority_ok': "✅ أنت في قائمة الأولوية!",
        'saved_ok': "✅ تم حفظ الرابط.",
        'match_msg': "🔗 تم العثور على تطابق!\n\n📌 رقم المهمة: #{code}\n\n🤝 رابط المستخدم الآخر:\n{link}\n\n⬆️ اضغط، ابدأ البوت، ثم ✅ سجلت.",
        'done_btn': "✅ سجلت",
        'already_btn': "⚠️ بدأت سابقاً",
        'confirm_msg': "📌 المهمة #{code}\n\n✅ المستخدم يؤكد التسجيل. هل تؤكد؟",
        'yes_btn': "✅ نعم",
        'retry_btn': "🔁 طلب إعادة المحاولة",
        'complete_msg': "✅ اكتملت المهمة! +1 نقطة! #{code}\n📊 اليوم: {tasks}/40",
        'retry_msg': "❌ يقول المستخدم أنك لم تسجل. اضغط على الرابط وابدأ البوت!",
        'new_link_req': "📤 قال المستخدم أنه بدأ البوت سابقاً.\n📌 رقم المهمة: #{code}\n\n<b>أرسل رابط إحالة جديد:</b>\nسيتم إرسال هذا الرابط إلى الطرف الآخر.",
        'new_link_ok': "✅ تم استلام رابط تعويضي!\n📌 رقم المهمة: #{code}\n\n🤝 الرابط التعويضي لك:\n{link}\n\n⬆️ اضغط، ابدأ البوت، ثم ✅ سجلت.",
        'points_info': "💎 نقاطك: {points}\n\n🔗 رابط الإحالة الخاص بك: {link}",
        'admin_prompt': "📝 اكتب رسالتك:",
        'admin_sent': "✅ تم الإرسال.",
        'stats': "📊 إحصائيات\n👥 المستخدمين: {users}\n✅ المهام: {tasks}",
        'admin_welcome': "👑 لوحة المدير",
        'broadcast_btn': "📢 بث للجميع",
        'private_btn': "👤 رسالة خاصة",
        'back_btn': "🔙 القائمة الرئيسية",
        'broadcast_prompt': "📢 اكتب الإعلان:",
        'invalid_link': "❌ رابط غير صالح!",
        'need_link': "❌ أرسل رابطاً أولاً!",
        'enter_id': "👤 أدخل المعرف:",
        'enter_msg': "💬 أدخل الرسالة:",
        'invalid_id': "❌ معرف غير صالح!",
        'private_ok': "✅ تم الإرسال.",
        'private_fail': "❌ فشل الإرسال!",
        'broadcast_ok': "✅ اكتمل البث!\n✅ نجاح: {ok}\n❌ فشل: {fail}",
        'new_msg': "📩 رسالة جديدة\n👤 {uid}\n💬 {msg}",
        'already_today': "❌ لقد أرسلت اليوم بالفعل!",
        'done_sent': "✅ تم إرسال إشعار 'سجلت' إلى الطرف الآخر!",
        'confirm_sent': "✅ تم إرسال التأكيد!",
        'already_sent': "✅ تم إرسال المعلومات! انتظار رابط جديد.",
        'waiting_both': "⏳ انتظار تأكيد كلا الطرفين...",
        'waiting_other': "⏳ انتظار تأكيد الطرف الآخر...",
        'both_confirmed': "✅ أكد كلا الطرفين! اكتملت المهمة!"
    }
}

# ========== VERİTABANI ==========
def get_db():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        lang TEXT DEFAULT 'tr',
        points INTEGER DEFAULT 0,
        daily INTEGER DEFAULT 0,
        last_date TEXT,
        ref_link TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS queue(
        user_id INTEGER PRIMARY KEY,
        ref_link TEXT,
        priority INTEGER DEFAULT 0,
        join_time INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS matches(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user1 INTEGER, user2 INTEGER,
        link1 TEXT, link2 TEXT,
        task_no TEXT,
        status1 TEXT DEFAULT 'pending',
        status2 TEXT DEFAULT 'pending',
        done1 INTEGER DEFAULT 0,
        done2 INTEGER DEFAULT 0,
        confirm1 INTEGER DEFAULT 0,
        confirm2 INTEGER DEFAULT 0)''')
    c.execute('''CREATE TABLE IF NOT EXISTS daily_ref(
        inviter INTEGER, invited INTEGER, date TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS waiting(
        user_id INTEGER PRIMARY KEY,
        requester INTEGER,
        match_id INTEGER,
        task_no TEXT)''')
    conn.commit()
    conn.close()

def get_lang(uid):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT lang FROM users WHERE user_id=?", (uid,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 'tr'

def set_lang(uid, lang):
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE users SET lang=? WHERE user_id=?", (lang, uid))
    conn.commit()
    conn.close()

def get_user(uid):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT ref_link, points, daily FROM users WHERE user_id=?", (uid,))
    row = c.fetchone()
    conn.close()
    return row if row else (None, 0, 0)

def save_link(uid, link):
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE users SET ref_link=? WHERE user_id=?", (link, uid))
    conn.commit()
    conn.close()

def in_queue(uid):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT user_id FROM queue WHERE user_id=?", (uid,))
    row = c.fetchone()
    conn.close()
    return row is not None

def add_queue(uid, link, prio=0):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM queue WHERE user_id=?", (uid,))
    c.execute("INSERT INTO queue VALUES(?, ?, ?, ?)", (uid, link, prio, int(time.time())))
    conn.commit()
    conn.close()

def remove_queue(uid):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM queue WHERE user_id=?", (uid,))
    conn.commit()
    conn.close()

def check_daily(uid):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT last_date, daily FROM users WHERE user_id=?", (uid,))
    row = c.fetchone()
    if row and row[0] == today:
        result = row[1] if row[1] else 0
        conn.close()
        return result
    else:
        c.execute("UPDATE users SET daily=0, last_date=? WHERE user_id=?", (today, uid))
        conn.commit()
        conn.close()
        return 0

def add_task(uid):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_db()
    c = conn.cursor()
    c.execute("UPDATE users SET daily=daily+1, points=points+1 WHERE user_id=?", (uid,))
    c.execute("UPDATE users SET last_date=? WHERE user_id=?", (today, uid))
    conn.commit()
    conn.close()

def check_daily_ref(inv, invd):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM daily_ref WHERE inviter=? AND invited=? AND date=?", (inv, invd, today))
    row = c.fetchone()
    conn.close()
    return row is not None

def add_daily_ref(inv, invd):
    today = datetime.now().strftime("%Y-%m-%d")
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT INTO daily_ref VALUES(?, ?, ?)", (inv, invd, today))
    conn.commit()
    conn.close()

def gen_task():
    return str(random.randint(10000, 99999))

def get_match(match_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT user1, user2, task_no, status1, status2, done1, done2, confirm1, confirm2 FROM matches WHERE id=?", (match_id,))
    row = c.fetchone()
    conn.close()
    return row

def update_match_done(match_id, user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT user1, user2, done1, done2 FROM matches WHERE id=?", (match_id,))
    row = c.fetchone()
    if row:
        u1, u2, d1, d2 = row
        if user_id == u1:
            c.execute("UPDATE matches SET done1=1, status1='done' WHERE id=?", (match_id,))
        else:
            c.execute("UPDATE matches SET done2=1, status2='done' WHERE id=?", (match_id,))
        conn.commit()
    conn.close()

def update_match_confirm(match_id, user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT user1, user2, confirm1, confirm2 FROM matches WHERE id=?", (match_id,))
    row = c.fetchone()
    if row:
        u1, u2, c1, c2 = row
        if user_id == u1:
            c.execute("UPDATE matches SET confirm1=1 WHERE id=?", (match_id,))
        else:
            c.execute("UPDATE matches SET confirm2=1 WHERE id=?", (match_id,))
        conn.commit()
    conn.close()

def is_match_completed(match_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT done1, done2, confirm1, confirm2 FROM matches WHERE id=?", (match_id,))
    row = c.fetchone()
    conn.close()
    if row:
        done1, done2, conf1, conf2 = row
        return done1 == 1 and done2 == 1 and conf1 == 1 and conf2 == 1
    return False

def set_waiting(uid, req, match_id, task_no):
    conn = get_db()
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO waiting VALUES(?, ?, ?, ?)", (uid, req, match_id, task_no))
    conn.commit()
    conn.close()

def get_waiting(uid):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT requester, match_id, task_no FROM waiting WHERE user_id=?", (uid,))
    row = c.fetchone()
    conn.close()
    return row

def clear_waiting(uid):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM waiting WHERE user_id=?", (uid,))
    conn.commit()
    conn.close()

def valid_link(link):
    return link.startswith("https://t.me/") and "?start=" in link and len(link.split("?start=")[1]) > 0

def make_clickable(link):
    return f'<a href="{link}">{link}</a>'

# ========== KLAVYELER ==========
def lang_kb():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("🇹🇷 Türkçe", callback_data="lang_tr"),
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        InlineKeyboardButton("🇩🇪 Deutsch", callback_data="lang_de"),
        InlineKeyboardButton("🇫🇷 Français", callback_data="lang_fr"),
        InlineKeyboardButton("🇪🇸 Español", callback_data="lang_es"),
        InlineKeyboardButton("🇸🇦 العربية", callback_data="lang_ar")
    )
    return kb

def join_kb(l):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("📢 KANALA KATIL", url="https://t.me/cryptoxd_ru"))
    kb.add(InlineKeyboardButton(t[l]['check'], callback_data="check"))
    return kb

def main_kb(uid, l):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(t[l]['ref_btn']))
    kb.add(KeyboardButton(t[l]['points_btn']))
    kb.add(KeyboardButton(t[l]['admin_btn']))
    kb.add(KeyboardButton(t[l]['stats_btn']))
    if uid == ADMIN_ID:
        kb.add(KeyboardButton(t[l]['admin_panel_btn']))
    return kb

def ref_kb(uid, l):
    kb = InlineKeyboardMarkup()
    if in_queue(uid):
        kb.add(InlineKeyboardButton(t[l]['exit'], callback_data="exit"))
    else:
        kb.add(InlineKeyboardButton(t[l]['join_q'], callback_data="join"))
    kb.add(InlineKeyboardButton(t[l]['change'], callback_data="change"))
    return kb

def priority_kb(l):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(t[l]['pay5'], callback_data="pay5"))
    kb.add(InlineKeyboardButton(t[l]['normal'], callback_data="normal"))
    return kb

def match_kb(l, other, match_id, task):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(f"✅ {t[l]['done_btn']} #{task}", callback_data=f"done_{other}_{match_id}_{task}"))
    kb.add(InlineKeyboardButton(f"⚠️ {t[l]['already_btn']} #{task}", callback_data=f"already_{other}_{match_id}_{task}"))
    return kb

def confirm_kb(l, user, match_id, task):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(f"✅ {t[l]['yes_btn']} #{task}", callback_data=f"confirm_{user}_{match_id}_{task}"))
    kb.add(InlineKeyboardButton(f"🔁 {t[l]['retry_btn']} #{task}", callback_data=f"retry_{user}_{match_id}_{task}"))
    return kb

def admin_kb(l):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton(t[l]['broadcast_btn']))
    kb.add(KeyboardButton(t[l]['private_btn']))
    kb.add(KeyboardButton(t[l]['stats_btn']))
    kb.add(KeyboardButton(t[l]['back_btn']))
    return kb

# ========== EŞLEŞME SİSTEMİ ==========
def match_users():
    time.sleep(1)
    conn = get_db()
    c = conn.cursor()
    
    c.execute("SELECT user_id, ref_link FROM queue ORDER BY priority DESC, join_time ASC")
    users = c.fetchall()
    
    if len(users) >= 2:
        user1 = users[0]
        user2 = None
        
        for u in users[1:]:
            if u[0] == user1[0]:
                continue
            
            c.execute("""
                SELECT link1, link2
                FROM matches
                WHERE (user1=? AND user2=?) OR (user1=? AND user2=?)
                ORDER BY id DESC
                LIMIT 1
            """, (user1[0], u[0], u[0], user1[0]))
            
            old_match = c.fetchone()
            can_match = True
            
            if old_match:
                old_link1, old_link2 = old_match
                user1_changed = (user1[1] != old_link1 and user1[1] != old_link2)
                user2_changed = (u[1] != old_link1 and u[1] != old_link2)
                if not (user1_changed and user2_changed):
                    can_match = False
            
            if can_match:
                user2 = u
                break
        
        if user2 and user1[1] and user2[1]:
            task = gen_task()
            c.execute("""INSERT INTO matches(user1, user2, link1, link2, task_no, 
                       status1, status2, done1, done2, confirm1, confirm2) 
                       VALUES(?,?,?,?,?,'pending','pending',0,0,0,0)""",
                      (user1[0], user2[0], user1[1], user2[1], task))
            conn.commit()
            match_id = c.lastrowid
            
            c.execute("DELETE FROM queue WHERE user_id=?", (user1[0],))
            c.execute("DELETE FROM queue WHERE user_id=?", (user2[0],))
            conn.commit()
            
            l1 = get_lang(user1[0])
            l2 = get_lang(user2[0])
            
            bot.send_message(user1[0], t[l1]['match_msg'].format(code=task, link=make_clickable(user2[1])), 
                           reply_markup=match_kb(l1, user2[0], match_id, task))
            bot.send_message(user2[0], t[l2]['match_msg'].format(code=task, link=make_clickable(user1[1])), 
                           reply_markup=match_kb(l2, user1[0], match_id, task))
    conn.close()

# ========== BAŞLAT ==========
@bot.message_handler(commands=['start'])
def start(m):
    uid = m.from_user.id
    args = m.text.split()
    inv = int(args[1]) if len(args) > 1 and args[1].isdigit() else None
    
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (uid,))
    if not c.fetchone():
        c.execute("INSERT INTO users(user_id, last_date, lang) VALUES(?, ?, 'tr')", (uid, datetime.now().strftime("%Y-%m-%d")))
        if inv and inv != uid:
            c.execute("UPDATE users SET points=points+1, daily=daily+1 WHERE user_id=?", (inv,))
            add_daily_ref(inv, uid)
            try:
                bot.send_message(inv, f"🎉 Yeni kullanıcı! +1 puan! ID: {uid}")
            except:
                pass
        conn.commit()
        bot.send_message(ADMIN_ID, f"🆕 Yeni kullanıcı: {uid}")
        bot.send_message(uid, t['tr']['select_lang'], reply_markup=lang_kb())
    else:
        l = get_lang(uid)
        bot.send_message(uid, t[l]['join'], reply_markup=join_kb(l))
    conn.close()

# ========== DİL ==========
@bot.callback_query_handler(func=lambda c: c.data.startswith("lang_"))
def lang_cb(c):
    l = c.data.split("_")[1]
    set_lang(c.from_user.id, l)
    bot.edit_message_text(t[l]['join'], c.message.chat.id, c.message.message_id, reply_markup=join_kb(l))
    bot.answer_callback_query(c.id)

# ========== KANAL KONTROL ==========
@bot.callback_query_handler(func=lambda c: c.data == "check")
def check_cb(c):
    uid = c.from_user.id
    l = get_lang(uid)
    
    not_joined = []
    for channel in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(channel, uid)
            if member.status not in ["member", "administrator", "creator"]:
                not_joined.append(channel)
        except:
            not_joined.append(channel)
    
    if not not_joined:
        bot.send_message(uid, t[l]['welcome'], reply_markup=main_kb(uid, l))
        bot.answer_callback_query(c.id)
    else:
        kb = InlineKeyboardMarkup()
        for channel in not_joined:
            kb.add(InlineKeyboardButton(f"📢 {channel} KANALINA KATIL", url=f"https://t.me/{channel[1:]}/"))
        kb.add(InlineKeyboardButton(t[l]['check'], callback_data="check"))
        bot.send_message(uid, "📢 TÜM KANALLARA KATILMAK ZORUNDASIN!", reply_markup=kb)
        bot.answer_callback_query(c.id)

# ========== REFERANS LİNKİM ==========
@bot.message_handler(func=lambda m: m.text in [t[l]['ref_btn'] for l in t])
def my_ref(m):
    uid = m.chat.id
    l = get_lang(uid)
    tasks = check_daily(uid)
    link, points, _ = get_user(uid)
    if tasks >= 40:
        bot.send_message(uid, t[l]['limit'])
        return
    if link:
        bot.send_message(uid, t[l]['my_link'].format(link=make_clickable(link), points=points, tasks=tasks), reply_markup=ref_kb(uid, l))
    else:
        bot.send_message(uid, t[l]['send_link'])

# ========== QUEUE ==========
@bot.callback_query_handler(func=lambda c: c.data in ["change", "exit", "join"])
def queue_cb(c):
    uid = c.from_user.id
    l = get_lang(uid)
    if c.data == "change":
        remove_queue(uid)
        bot.edit_message_text(t[l]['changed'], c.message.chat.id, c.message.message_id)
    elif c.data == "exit":
        remove_queue(uid)
        bot.edit_message_text(t[l]['exited'], c.message.chat.id, c.message.message_id)
    elif c.data == "join":
        link, _, _ = get_user(uid)
        if not link:
            bot.answer_callback_query(c.id, t[l]['need_link'], show_alert=True)
            return
        add_queue(uid, link, 0)
        bot.edit_message_text(t[l]['joined'], c.message.chat.id, c.message.message_id)
        threading.Thread(target=match_users, daemon=True).start()
    bot.answer_callback_query(c.id)

# ========== LİNK KAYDET (DÜZELTİLDİ - TELAFİ LİNKİ) ==========
@bot.message_handler(func=lambda m: m.text and "https://t.me/" in m.text)
def save(m):
    uid = m.chat.id
    link = m.text
    l = get_lang(uid)
    
    if not valid_link(link):
        bot.send_message(uid, t[l]['invalid_link'])
        return
    
    # BEKLEYEN VAR MI? (ÖNCEDEN BAŞLATMIŞIM BUTONUNDAN)
    wait = get_waiting(uid)
    if wait:
        requester, old_match_id, task_no = wait
        clear_waiting(uid)
        
        # LİNKİ KAYDETME! SADECE KARŞI TARAFA İLET
        # save_link(uid, link) - BU SATIR YOK! LİNK KAYDEDİLMEZ!
        
        # TELAFİ LİNKİNİ KARŞI TARAFA GÖNDER (requester = link isteyen kişi)
        req_l = get_lang(requester)
        bot.send_message(requester, t[req_l]['new_link_ok'].format(code=task_no, link=make_clickable(link)), 
                        reply_markup=match_kb(req_l, uid, old_match_id, task_no))
        
        # LİNKİ GÖNDERENE BİLDİRİM (linki karşı tarafa ilettik)
        bot.send_message(uid, t[l]['saved_ok'])
        
        print(f"✅ TELAFİ LİNKİ İLETİLDİ: {uid} -> {requester} | Görev: #{task_no}")
        return
    
    # NORMAL KAYIT (bekleyen yoksa)
    tasks = check_daily(uid)
    if tasks >= 40:
        bot.send_message(uid, t[l]['limit'])
        return
    
    save_link(uid, link)
    add_queue(uid, link, 0)
    bot.send_message(uid, t[l]['fast_q'], reply_markup=priority_kb(l))

# ========== PUANLAR ==========
@bot.message_handler(func=lambda m: m.text in [t[l]['points_btn'] for l in t])
def points(m):
    uid = m.chat.id
    l = get_lang(uid)
    _, points, _ = get_user(uid)
    link = f"https://t.me/{BOT_USERNAME}?start={uid}"
    bot.send_message(uid, t[l]['points_info'].format(points=points, link=make_clickable(link)))

# ========== ADMİNE MESAJ ==========
wait_admin = {}
@bot.message_handler(func=lambda m: m.text in [t[l]['admin_btn'] for l in t])
def admin_req(m):
    l = get_lang(m.chat.id)
    wait_admin[m.chat.id] = True
    bot.send_message(m.chat.id, t[l]['admin_prompt'])

@bot.message_handler(func=lambda m: m.chat.id in wait_admin)
def admin_send(m):
    uid = m.chat.id
    l = get_lang(uid)
    bot.send_message(ADMIN_ID, t[l]['new_msg'].format(uid=uid, msg=m.text))
    del wait_admin[uid]
    bot.send_message(uid, t[l]['admin_sent'])

# ========== İSTATİSTİK ==========
@bot.message_handler(func=lambda m: m.text in [t[l]['stats_btn'] for l in t])
def stats(m):
    l = get_lang(m.chat.id)
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM users")
    users = c.fetchone()[0]
    c.execute("SELECT COUNT(*) FROM matches WHERE done1=1 AND done2=1 AND confirm1=1 AND confirm2=1")
    tasks = c.fetchone()[0]
    conn.close()
    bot.send_message(m.chat.id, t[l]['stats'].format(users=users, tasks=tasks))

# ========== ADMIN PANEL ==========
@bot.message_handler(func=lambda m: m.text == "👑 Admin Panel" and m.from_user.id == ADMIN_ID)
def admin_panel(m):
    l = get_lang(m.chat.id)
    bot.send_message(m.chat.id, t[l]['admin_welcome'], reply_markup=admin_kb(l))

@bot.message_handler(func=lambda m: m.text == "🔙 Ana Menü" and m.from_user.id == ADMIN_ID)
def back(m):
    l = get_lang(m.chat.id)
    bot.send_message(m.chat.id, t[l]['welcome'], reply_markup=main_kb(m.chat.id, l))

# ========== BROADCAST ==========
broad = {}
@bot.message_handler(func=lambda m: m.text == "📢 Duyuru" and m.from_user.id == ADMIN_ID)
def broad_req(m):
    broad[m.chat.id] = "broad"
    bot.send_message(m.chat.id, t['tr']['broadcast_prompt'])

@bot.message_handler(func=lambda m: m.text == "👤 Özel Mesaj" and m.from_user.id == ADMIN_ID)
def private_req(m):
    broad[m.chat.id] = "id"
    bot.send_message(m.chat.id, t['tr']['enter_id'])

@bot.message_handler(func=lambda m: m.from_user.id == ADMIN_ID and m.chat.id in broad)
def handle_admin(m):
    uid = m.chat.id
    state = broad[uid]
    if state == "broad":
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT user_id FROM users")
        users = c.fetchall()
        conn.close()
        ok, fail = 0, 0
        for u in users:
            try:
                l = get_lang(u[0])
                bot.send_message(u[0], f"📢 {t[l]['broadcast_btn']}\n\n{m.text}")
                ok += 1
                time.sleep(0.05)
            except:
                fail += 1
        del broad[uid]
        bot.send_message(uid, t['tr']['broadcast_ok'].format(ok=ok, fail=fail))
    elif state == "id":
        try:
            target = int(m.text)
            broad[uid] = ("msg", target)
            bot.send_message(uid, t['tr']['enter_msg'])
        except:
            del broad[uid]
            bot.send_message(uid, t['tr']['invalid_id'])
    elif isinstance(state, tuple) and state[0] == "msg":
        target = state[1]
        try:
            l = get_lang(target)
            bot.send_message(target, f"📨 {t[l]['admin_btn']}\n\n{m.text}")
            bot.send_message(uid, t['tr']['private_ok'])
        except:
            bot.send_message(uid, t['tr']['private_fail'])
        del broad[uid]

# ========== HIZLI EŞLEŞME ==========
@bot.callback_query_handler(func=lambda c: c.data in ["pay5", "normal"])
def fast_cb(c):
    uid = c.from_user.id
    l = get_lang(uid)
    link, points, _ = get_user(uid)
    if not link:
        bot.answer_callback_query(c.id, t[l]['need_link'], show_alert=True)
        return
    if c.data == "pay5":
        if points < 5:
            bot.send_message(uid, t[l]['no_points'].format(points=points))
            bot.answer_callback_query(c.id)
            return
        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE users SET points=points-5 WHERE user_id=?", (uid,))
        conn.commit()
        conn.close()
        add_queue(uid, link, 1)
        bot.send_message(uid, t[l]['priority_ok'])
    else:
        add_queue(uid, link, 0)
        bot.send_message(uid, t[l]['saved_ok'])
    bot.delete_message(c.message.chat.id, c.message.message_id)
    bot.answer_callback_query(c.id)
    threading.Thread(target=match_users, daemon=True).start()

# ========== EŞLEŞME BUTONLARI ==========
@bot.callback_query_handler(func=lambda c: c.data.startswith("done_"))
def done_cb(c):
    parts = c.data.split("_")
    other = int(parts[1])
    match_id = int(parts[2])
    task = parts[3]
    uid = c.from_user.id
    l = get_lang(uid)
    
    try:
        bot.edit_message_reply_markup(c.message.chat.id, c.message.message_id, reply_markup=None)
    except:
        pass
    
    match = get_match(match_id)
    if not match:
        bot.send_message(uid, f"❌ Eşleşme bulunamadı!")
        bot.answer_callback_query(c.id)
        return
    
    user1, user2, task_no, status1, status2, done1, done2, conf1, conf2 = match
    
    if (uid == user1 and done1 == 1) or (uid == user2 and done2 == 1):
        bot.send_message(uid, "❌ Zaten 'Kayıt Oldum' dediniz!")
        bot.answer_callback_query(c.id)
        return
    
    update_match_done(match_id, uid)
    
    other_user = user2 if uid == user1 else user1
    other_l = get_lang(other_user)
    bot.send_message(other_user, t[other_l]['waiting_other'])
    bot.send_message(uid, t[l]['waiting_other'])
    
    new_match = get_match(match_id)
    if new_match:
        _, _, _, _, _, new_done1, new_done2, _, _ = new_match
        if new_done1 == 1 and new_done2 == 1:
            bot.send_message(user1, t[get_lang(user1)]['confirm_msg'].format(code=task_no), 
                           reply_markup=confirm_kb(get_lang(user1), user2, match_id, task_no))
            bot.send_message(user2, t[get_lang(user2)]['confirm_msg'].format(code=task_no), 
                           reply_markup=confirm_kb(get_lang(user2), user1, match_id, task_no))
    
    bot.answer_callback_query(c.id, t[l]['done_sent'])

# ========== CONFIRM BUTONU ==========
@bot.callback_query_handler(func=lambda c: c.data.startswith("confirm_"))
def confirm_cb(c):
    parts = c.data.split("_")
    other = int(parts[1])
    match_id = int(parts[2])
    task = parts[3]
    uid = c.from_user.id
    l = get_lang(uid)
    
    try:
        bot.edit_message_reply_markup(c.message.chat.id, c.message.message_id, reply_markup=None)
    except:
        pass
    
    match = get_match(match_id)
    if not match:
        bot.send_message(uid, "❌ Eşleşme bulunamadı!")
        bot.answer_callback_query(c.id)
        return
    
    user1, user2, task_no, status1, status2, done1, done2, conf1, conf2 = match
    
    if (uid == user1 and conf1 == 1) or (uid == user2 and conf2 == 1):
        bot.send_message(uid, "❌ Zaten onay verdiniz!")
        bot.answer_callback_query(c.id)
        return
    
    update_match_confirm(match_id, uid)
    
    other_user = user2 if uid == user1 else user1
    other_l = get_lang(other_user)
    bot.send_message(other_user, t[other_l]['waiting_other'])
    bot.send_message(uid, t[l]['waiting_other'])
    
    if is_match_completed(match_id):
        if check_daily(user1) >= 40 or check_daily(user2) >= 40:
            bot.send_message(user1, t[get_lang(user1)]['limit'])
            bot.send_message(user2, t[get_lang(user2)]['limit'])
            bot.answer_callback_query(c.id)
            return
        
        add_task(user1)
        add_task(user2)
        add_daily_ref(user1, user2)
        
        link1, _, _ = get_user(user1)
        link2, _, _ = get_user(user2)
        
        if link1:
            add_queue(user1, link1, 0)
        if link2:
            add_queue(user2, link2, 0)
        
        threading.Thread(target=match_users, daemon=True).start()
        
        conn = get_db()
        c2 = conn.cursor()
        c2.execute("SELECT daily FROM users WHERE user_id=?", (user1,))
        tasks1 = c2.fetchone()[0]
        c2.execute("SELECT daily FROM users WHERE user_id=?", (user2,))
        tasks2 = c2.fetchone()[0]
        conn.close()
        
        bot.send_message(user1, t[get_lang(user1)]['complete_msg'].format(code=task_no, tasks=tasks1))
        bot.send_message(user2, t[get_lang(user2)]['complete_msg'].format(code=task_no, tasks=tasks2))
        bot.send_message(user1, t[get_lang(user1)]['both_confirmed'])
        bot.send_message(user2, t[get_lang(user2)]['both_confirmed'])
    
    bot.answer_callback_query(c.id, t[l]['confirm_sent'])

# ========== RETRY BUTONU ==========
@bot.callback_query_handler(func=lambda c: c.data.startswith("retry_"))
def retry_cb(c):
    parts = c.data.split("_")
    other = int(parts[1])
    match_id = int(parts[2])
    task = parts[3]
    uid = c.from_user.id
    l = get_lang(other)
    
    try:
        bot.edit_message_reply_markup(c.message.chat.id, c.message.message_id, reply_markup=None)
    except:
        pass
    
    match = get_match(match_id)
    if not match:
        bot.send_message(uid, "❌ Eşleşme bulunamadı!")
        bot.answer_callback_query(c.id)
        return
    
    user1, user2, _, _, _, _, _, _, _ = match
    other_user = user2 if uid == user1 else user1
    
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton(f"✅ {t[l]['done_btn']} #{task}", callback_data=f"done_{uid}_{match_id}_{task}"))
    kb.add(InlineKeyboardButton(f"✅ {t[l]['yes_btn']} #{task}", callback_data=f"confirm_{uid}_{match_id}_{task}"))
    bot.send_message(other_user, t[l]['retry_msg'], reply_markup=kb)
    bot.answer_callback_query(c.id)

# ========== ALREADY BUTONU ==========
@bot.callback_query_handler(func=lambda c: c.data.startswith("already_"))
def already_cb(c):
    parts = c.data.split("_")
    other = int(parts[1])
    match_id = int(parts[2])
    task = parts[3]
    uid = c.from_user.id
    l = get_lang(other)
    
    try:
        bot.edit_message_reply_markup(c.message.chat.id, c.message.message_id, reply_markup=None)
    except:
        pass
    
    match = get_match(match_id)
    if match:
        user1, user2, task_no, _, _, _, _, _, _ = match
        other_user = user2 if uid == user1 else user1
        
        # Yeni link beklensin
        set_waiting(other_user, uid, match_id, task_no)
        bot.send_message(other_user, t[l]['new_link_req'].format(code=task_no))
        bot.send_message(uid, t[get_lang(uid)]['already_sent'])
    bot.answer_callback_query(c.id)

# ========== MAIN ==========
def main():
    if not os.path.exists(DB_PATH):
        init_db()
        print("✅ Yeni database oluşturuldu!")
    else:
        print("✅ Database mevcut, veriler korunuyor!")
    print("=" * 60)
    print("🚀 BOT BAŞLADI - TAM EKSİKSİZ!")
    print(f"📌 Bot: @{BOT_USERNAME}")
    print(f"👑 Admin: {ADMIN_ID}")
    print("🌍 7 DİL: TR, RU, EN, DE, FR, ES, AR")
    print("✅ TELAFİ LİNK SİSTEMİ: Link karşı tarafa gider, kaydedilmez")
    print("✅ Çift taraflı onay sistemi aktif")
    print("=" * 60)
    bot.infinity_polling(timeout=80)

if __name__ == "__main__":
    main()