from aiogram import F
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InputMediaPhoto
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import keyboards as kb
from config import Hellomsg, We
import aiosqlite
from aiogram.types import CallbackQuery

# from config import PAYMENT_TOKEN
# from aiogram.methods import SendInvoice


router = Router()

class Reg(StatesGroup):
    name = State()
    number = State()

class Rent(StatesGroup):
    type = State()
    district = State()
    town = State()
    price = State()
    area = State()
    rooms = State()
    description = State()
    photo = State()
class Find(StatesGroup):
    findtype = State() 
    findtown = State()
    finddistrict = State()
    pricemin = State()
    pricemax = State()
    areamin = State()
    areamax = State()
    findrooms = State()
    findroomsmax = State()
class Edit(StatesGroup):
    edit_field = State()
    edit_value = State()
    
@router.message(F.text == "🔙 Назад в главное меню")
async def back(message: Message, state: FSMContext):
    await message.answer("Вы вернулись в главное меню", reply_markup=kb.main)
    await state.clear()



#Регистрация
async def initialize_database():
    async with aiosqlite.connect('bot_database.db') as db:
        await db.execute("CREATE TABLE IF NOT EXISTS users (telegram_id INTEGER, name TEXT, number TEXT)")
        await db.execute("CREATE TABLE IF NOT EXISTS rent (telegram_id INTEGER, town TEXT, district TEXT, type TEXT, area INTEGER, rooms INTEGER, price INTEGER, description TEXT, photo BLOB)")
        await db.execute("CREATE TABLE IF NOT EXISTS favorites (telegram_id INTEGER, town TEXT, district TEXT, type TEXT, area INTEGER, rooms INTEGER, price INTEGER, description TEXT, photo BLOB)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_users_telegram_id ON users (telegram_id)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_rent_town ON rent (town)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_rent_district ON rent (district)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_rent_type ON rent (type)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_rent_rooms ON rent (rooms)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_rent_area ON rent (area)")
        await db.execute("CREATE INDEX IF NOT EXISTS idx_rent_price ON rent (price)")
        await db.commit()

async def add_to_database(telegram_id, name, number):
    async with aiosqlite.connect('bot_database.db') as db:
        cursor = await db.execute('SELECT * FROM users WHERE telegram_id = ?', (telegram_id,))
        data = await cursor.fetchone()
        if data is not None:
           return
        await db.execute("INSERT INTO users (telegram_id, name, number) VALUES (?, ?, ?)", (telegram_id, name, number))
        await db.commit()

async def add_to_database_rent(telegram_id, town, district, property_type, area, rooms, price, description, photos):
    valid_photos = ','.join([photo for photo in photos if all(c.isalnum() or c in '-_' for c in photo) and len(photo) > 0])
    async with aiosqlite.connect('bot_database.db') as db:
        await db.execute("INSERT INTO rent (telegram_id, town, district, type, area, rooms, price, description, photo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (telegram_id, town, district, property_type, area, rooms, price, description, valid_photos))
        await db.commit()

@router.message(F.text == "📝 Зарегистрироваться")
async def reg1(message: Message, state: FSMContext):
    async with aiosqlite.connect('bot_database.db') as db:
        cursor = await db.execute('SELECT * FROM users WHERE telegram_id = ?', (message.from_user.id,))
        data = await cursor.fetchone()
        if data is not None:
            await message.answer("Вы уже зарегистрированы.", reply_markup=kb.main)
            return
    await state.set_state(Reg.name)
    await message.answer("Отправьте ваше имя")

@router.message(Reg.name)
async def reg2(message: Message, state: FSMContext):
        await state.update_data(name=message.text)
        await state.set_state(Reg.number)
        await message.answer("Отправьте ваш контакт", reply_markup=kb.contact)

@router.message(Reg.number, F.contact)
async def reg3(message: Message, state: FSMContext):
    if message.contact:
        phone_number = message.contact.phone_number
        if not phone_number.startswith("+"):
            phone_number = "+" + phone_number
        await state.update_data(number=phone_number)
        data = await state.get_data()
        await message.answer(f"Спасибо за регистрацию. \nИмя: {data['name']}\nНомер Телефона: {data['number']}",
                             reply_markup=kb.main)
        await add_to_database(message.from_user.id, data['name'], data['number'])
        await state.clear()
    else:
        await message.answer("Пожалуйста, отправьте ваш контакт.")

#Start
@router.message(CommandStart())
async def start(message: Message):
    await message.answer(Hellomsg, reply_markup=kb.main)
                         

#Сдать в Аренду                          
@router.message(F.text == "🗝️ Сдать квартиру")
async def rent_town(message: Message, state: FSMContext):
    async with aiosqlite.connect('bot_database.db') as db:
        cursor = await db.execute('SELECT * FROM users WHERE telegram_id = ?', (message.from_user.id,))
        data = await cursor.fetchone()
        if data is None:
            await message.answer("Вы не зарегистрированы. Пожалуйста, зарегистрируйтесь, чтобы продолжить.", reply_markup=kb.main)
            return
    await state.update_data(photos=[])
    await state.set_state(Rent.town)
    await message.answer("В каком городе Узбекистана вы хотите сдать жилье?",
                         reply_markup=kb.Town2)
        

@router.message(Rent.town)
async def rent_district(message: Message, state: FSMContext):
    await state.update_data(town=message.text)
    await state.set_state(Rent.district)
    if message.text == "Ташкент":
        await message.answer("Укажите район, где находится ваше жилье.",
                             reply_markup=kb.tdists1)
    elif message.text == "Самарканд":
        await message.answer('Укажите район, где находится ваше жилье.',
                             reply_markup=kb.sdists1)

@router.message(Rent.district)
async def rent_type(message: Message, state: FSMContext):
    await state.update_data(district=message.text)
    await state.set_state(Rent.type)
    await message.answer("Выберите тип жилья:",
                         reply_markup=kb.type)

@router.message(Rent.type)
async def rent_rooms(message: Message, state: FSMContext):
    await state.update_data(type=message.text)
    await state.set_state(Rent.rooms)
    await message.answer("Сколько комнат в вашем жилье?",
                         reply_markup=kb.back)

@router.message(Rent.rooms)
async def rent_area(message: Message, state: FSMContext):
    await state.update_data(rooms=message.text)
    await state.set_state(Rent.area)
    await message.answer("Введите площадь в м² (например, 50).")

@router.message(Rent.area)
async def rent_price(message: Message, state: FSMContext):
    await state.update_data(area=message.text)
    await state.set_state(Rent.price)
    await message.answer("Укажите цену в долларах США за месяц аренды")

@router.message(Rent.price)
async def rent_description(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(Rent.description)
    await message.answer("Расскажите о вашем жилье: есть ли мебель, техника, Wi-Fi и другие удобства?")

@router.message(Rent.description)
async def rent_photo(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Прикрепите фото жилья")
    await state.set_state(Rent.photo)

@router.message(Rent.photo, F.photo)
async def add_photo(message: Message, state: FSMContext):
    rent_data = await state.get_data()
    photos = rent_data.get('photos', [])
    file_id = message.photo[-1].file_id
    if all(c.isalnum() or c in '-_' for c in file_id):
        photos.append(file_id)
        await state.update_data(photos=photos)
        await message.answer("Фото добавлено. Если хотите добавить еще фото, прикрепите его. Если нет, нажмите 'Подтвердить'", reply_markup=kb.add_more_photos_or_finish)
    else:
        await message.answer("Неверный идентификатор файла. Попробуйте снова.")

@router.message(Rent.photo, F.text == "Подтвердить")
async def finish_rent(message: Message, state: FSMContext):
    rent_data = await state.get_data()
    photos = rent_data.get('photos', [])
    if photos:
        media_group = [InputMediaPhoto(media=photo) for photo in photos if all(c.isalnum() or c in '-_' for c in photo) and len(photo) > 0]
        await message.answer_media_group(media_group)
        await message.answer(f"Город: {rent_data['town']}\nРайон: {rent_data['district']}\nТип Жилья: {rent_data['type']}\nЦена: {rent_data['price']}\nПлощадь: {rent_data['area']}\nКомнаты: {rent_data['rooms']}\nОписание: {rent_data['description']}\n✅ Объявление готово!")
    else:
        await message.answer("Нет фото для отображения.")
    
    await add_to_database_rent(message.from_user.id, rent_data['town'], rent_data['district'], rent_data['type'], rent_data['area'], rent_data['rooms'], rent_data['price'], rent_data['description'], photos)
    await state.clear()
    await message.answer("Ваше объявление успешно опубликовано!", reply_markup=kb.main)

@router.message(F.text == "Изменить")
async def edit_rent_data(message: Message, state: FSMContext):
    rent_data = await state.get_data()
    await message.answer(f"Текущие данные:\nГород: {rent_data['town']}\nРайон: {rent_data['district']}\nТип Жилья: {rent_data['type']}\nЦена: {rent_data['price']}\nПлощадь: {rent_data['area']}\nКомнаты: {rent_data['rooms']}\nОписание: {rent_data['description']}\n\nВведите номер поля, которое хотите изменить:\n1. Город\n2. Район\n3. Тип Жилья\n4. Цена\n5. Площадь\n6. Комнаты\n7. Описание\n8. Фото", reply_markup=kb.main)
    await state.set_state(Edit.edit_field)

@router.message(Edit.edit_field)
async def edit_field(message: Message, state: FSMContext):
    field_number = message.text
    fields = {
        "1": "town",
        "2": "district",
        "3": "type",
        "4": "price",
        "5": "area",
        "6": "rooms",
        "7": "description",
        "8": "photo"
    }
    if field_number in fields:
        await state.update_data(edit_field=fields[field_number])
        if fields[field_number] == "photo":
            await message.answer("Прикрепите новое фото жилья")
        else:
            await message.answer(f"Введите новое значение для {fields[field_number]}")
        await state.set_state(Edit.edit_value)
    else:
        await message.answer("Неверный номер поля. Попробуйте снова.")

@router.message(Edit.edit_value)
async def edit_value(message: Message, state: FSMContext):
    data = await state.get_data()
    edit_field = data.get('edit_field')

    if edit_field == "photo":
        if message.photo:
            photos = data.get('photos', [])
            photos.append(message.photo[-1].file_id)
            await state.update_data(photos=photos)
        else:
            await message.answer("Пожалуйста, прикрепите фото.")
            return
    else:
        await state.update_data({edit_field: message.text})

    rent_data = await state.get_data()
    photos = rent_data.get('photos', [])
    media_group = [InputMediaPhoto(media=photo) for photo in photos]
    await message.answer_media_group(media_group)
    await message.answer(f"Город: {rent_data['town']}\nРайон: {rent_data['district']}\nТип Жилья: {rent_data['type']}\nЦена: {rent_data['price']}\nПлощадь: {rent_data['area']}\nКомнаты: {rent_data['rooms']}\nОписание: {rent_data['description']}\nОбъявление готово!",
                         reply_markup=kb.main)
    await message.answer("Если все данные верны, нажмите 'Подтвердить'. Если хотите изменить данные, нажмите 'Изменить'.", reply_markup=kb.confirm_or_edit)
    await state.set_state(Rent.photo)



   
#Найти квартиру
@router.message(F.text == "🏠 Найти квартиру")
async def findtown(message: Message, state: FSMContext):
    async with aiosqlite.connect('bot_database.db') as db:
        cursor = await db.execute('SELECT * FROM users WHERE telegram_id = ?', (message.from_user.id,))
        data = await cursor.fetchone()
        if data is None:
            await message.answer("Вы не зарегистрированы. Пожалуйста, зарегистрируйтесь, чтобы продолжить.", reply_markup=kb.main)
            return
    await state.set_state(Find.findtown)
    await message.answer("Введите город Узбекистана", reply_markup=kb.Town2)
    

@router.message(Find.findtown)
async def finddistrict(message: Message, state: FSMContext):
    await state.update_data(findtown=message.text)
    await state.set_state(Find.finddistrict)
    if message.text == "Ташкент":
        await message.answer("Введите район, в котором вы хотели бы снять квартиру",
                             reply_markup=kb.tdists2)
    elif message.text == "Самарканд":
        await message.answer("Введите район, в котором вы хотели бы снять квартиру",
                             reply_markup=kb.sdists2)

@router.message(Find.finddistrict)
async def findtype(message: Message, state: FSMContext):
    await state.update_data(finddistrict=message.text)
    await state.set_state(Find.findtype)
    await message.answer("Квартира, Дом или Комната",
                         reply_markup=kb.type)

@router.message(Find.findtype)
async def findrooms(message: Message, state: FSMContext):
    await state.update_data(findtype=message.text)
    await state.set_state(Find.findrooms)
    await message.answer("Введите минимальное количество комнат",
                         reply_markup=kb.back)

@router.message(Find.findrooms)
async def findroomsmax(message: Message, state: FSMContext):
    await state.update_data(findrooms=message.text)
    await state.set_state(Find.findroomsmax)
    await message.answer("Введите максимальное количество комнат")

@router.message(Find.findroomsmax)
async def findarea(message: Message, state: FSMContext):
    await state.update_data(findroomsmax=message.text)
    await state.set_state(Find.areamin)
    await message.answer("Введите минимальную площадь")

@router.message(Find.areamin)
async def findareamax(message: Message, state: FSMContext):
    await state.update_data(areamin=message.text)
    await state.set_state(Find.areamax)
    await message.answer("Введите максимальную площадь")

@router.message(Find.areamax)
async def findpricemin(message: Message, state: FSMContext):
    await state.update_data(areamax=message.text)
    await state.set_state(Find.pricemin)
    await message.answer("Введите минимальную цену")

@router.message(Find.pricemin)
async def findpricemax(message: Message, state: FSMContext):
    await state.update_data(pricemin=message.text)
    await state.set_state(Find.pricemax)
    await message.answer("Введите максимальную цену")

@router.message(Find.pricemax)
async def find_results(message: Message, state: FSMContext):
    await state.update_data(pricemax=message.text)
    search_data = await state.get_data()
    
    district_query = "%" if search_data['finddistrict'].lower() == "любой район" else search_data['finddistrict']
    
    async with aiosqlite.connect('bot_database.db') as db:
        cursor = await db.execute(
            "SELECT rent.town, rent.district, rent.type, rent.area, rent.rooms, rent.price, rent.description, rent.photo, users.number FROM rent JOIN users ON rent.telegram_id = users.telegram_id WHERE rent.town = ? AND rent.district LIKE ? AND rent.type = ? AND rent.rooms BETWEEN ? AND ? AND rent.area BETWEEN ? AND ? AND rent.price BETWEEN ? AND ?",
            (search_data['findtown'], district_query, search_data['findtype'], search_data['findrooms'], search_data['findroomsmax'], search_data['areamin'], search_data['areamax'], search_data['pricemin'], search_data['pricemax'])
        )
        results = await cursor.fetchall()
    
    if results:
        await state.update_data(results=results, current_index=0)
        await show_next_result(message, state)
    else:
        await message.answer("К сожалению, подходящих предложений не найдено.", reply_markup=kb.main)
        await state.clear()

async def show_next_result(message: Message, state: FSMContext):
    data = await state.get_data()
    results = data['results']
    current_index = data.get('current_index', 0)
    if current_index < len(results):
        result = results[current_index]
        photos = result[7].split(',')
        media_group = [InputMediaPhoto(media=photo) for photo in photos]
        try:
            await message.answer_media_group(media_group)
            await message.answer(
                text=f"Город: {result[0]}\nРайон: {result[1]}\nТип жилья: {result[2]}\nПлощадь: {result[3]}\nКомнаты: {result[4]}\nЦена: {result[5]}\nОписание: {result[6]}\nКонтактный номер: {result[8]}",
                reply_markup=kb.add_to_favorites_or_skip
            )
        except Exception as e:
            await message.answer(f"Ошибка при загрузке фото: {e}")
        await state.update_data(current_index=current_index + 1)

@router.callback_query(F.data == "previous_result")
async def previous_result(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_index = data.get('current_index', 0)
    if current_index > 1:
        await state.update_data(current_index=current_index - 2)
        await show_next_result(callback_query.message, state)
    else:
        await callback_query.answer("Это первое объявление.", show_alert=True)

@router.callback_query(F.data == "skip")
async def skip_result(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_index = data.get('current_index', 0)
    results = data.get('results', [])
    
    if current_index >= len(results):
        await callback_query.answer("Это были все результаты.", reply_markup=kb.main, show_alert=True)
        return
    
    await show_next_result(callback_query.message, state)

@router.callback_query(F.data == "add_to_favorites")
async def add_to_favorites(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_index = data.get('current_index', 0)
    results = data.get('results', [])
    
    if current_index > 0 and current_index <= len(results):
        result = results[current_index - 1]
        photos = result[7].split(',')
        async with aiosqlite.connect('bot_database.db') as db:
            await db.execute(
                "INSERT INTO favorites (telegram_id, town, district, type, area, rooms, price, description, photo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (callback_query.from_user.id, result[0], result[1], result[2], result[3], result[4], result[5], result[6], ','.join(photos))
            )
            await db.commit()
        await callback_query.answer("Объявление добавлено в избранное!")
        await show_next_result(callback_query.message, state)
    else:
        await callback_query.answer("Ошибка: неверный индекс результата.", show_alert=True)



@router.message(F.text == "⭐ Избранное")
async def show_favorites(message: Message, state: FSMContext):
    async with aiosqlite.connect('bot_database.db') as db:
        cursor = await db.execute('SELECT town, district, type, area, rooms, price, description, photo FROM favorites WHERE telegram_id = ?', (message.from_user.id,))
        favorites = await cursor.fetchall()

        if favorites:
            await state.update_data(favorites=favorites, current_index=0)
            await show_next_favorite(message, state)
        else:
            await message.answer("У вас нет избранных объявлений.", reply_markup=kb.main)

async def show_next_favorite(message: Message, state: FSMContext):
    data = await state.get_data()
    favorites = data.get('favorites', [])
    current_index = data.get('current_index', 0)

    if current_index < len(favorites):
        favorite = favorites[current_index]
        photos = favorite[7].split(',')
        media_group = [InputMediaPhoto(media=photo) for photo in photos]
        try:
            await message.answer_media_group(media_group)
            await message.answer(
                f"Город: {favorite[0]}\nРайон: {favorite[1]}\nТип жилья: {favorite[2]}\nПлощадь: {favorite[3]}\nКомнаты: {favorite[4]}\nЦена: {favorite[5]}\nОписание: {favorite[6]}",
                reply_markup=kb.next
            )
        except Exception as e:
            await message.answer(f"Ошибка при загрузке фото: {e}")
        await state.update_data(current_index=current_index + 1)
    else:
        await state.clear()

@router.callback_query(F.data == "previous")
async def previous_favorite(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_index = data.get('current_index')
    if current_index is not None and current_index > 1:
        await state.update_data(current_index=current_index - 2)
        await show_next_favorite(callback_query.message, state)
    else:
        await callback_query.answer("Это первое объявление.", show_alert=True)


#О нас
@router.message(F.text == "📎 О Нас")
async def Onas(message:Message):
    await message.answer(We, reply_markup=kb.main)


#Личный кабинет
@router.message(F.text == "👤 Личный кабинет")
async def personal_account(message: Message):
    async with aiosqlite.connect('bot_database.db') as db:
        cursor = await db.execute('SELECT name, number FROM users WHERE telegram_id = ?', (message.from_user.id,))
        user_data = await cursor.fetchone()
        if user_data:
            await message.answer(f"Ваши данные:\nИмя: {user_data[0]}\nНомер: {user_data[1]}", reply_markup=kb.ads)
        else:
            await message.answer("Пожалуйсто зарегистрируйтесь.", reply_markup=kb.ads)



#Модерация
class Moderate(StatesGroup):
    moderate_action = State()
    
@router.message(F.text == "/moderate")
async def moderate_start(message: Message, state: FSMContext):
    admin_ids = [1005986947, 768613544, 1116483191]
    if message.from_user.id not in admin_ids:
        await message.answer("У вас нет прав для выполнения этой команды.", reply_markup=kb.main)
        return
    async with aiosqlite.connect('bot_database.db') as db:
        cursor = await db.execute('SELECT rowid, town, district, type, area, rooms, price, description, photo FROM rent')
        rent_data = await cursor.fetchall()
        if rent_data:
            await state.update_data(rent_data=rent_data, current_index=0)
            await show_next_moderate(message, state)
        else:
            await message.answer("Нет объявлений для модерации.", reply_markup=kb.main)

async def show_next_moderate(message: Message, state: FSMContext):
    data = await state.get_data()
    rent_data = data.get('rent_data', [])
    current_index = data.get('current_index', 0)
    
    if current_index < len(rent_data):
        rent = rent_data[current_index]
        new_caption = f"ID: {rent[0]}\nГород: {rent[1]}\nРайон: {rent[2]}\nТип Жилья: {rent[3]}\nПлощадь: {rent[4]}\nКомнаты: {rent[5]}\nЦена: {rent[6]}\nОписание: {rent[7]}"
        photos = rent[8].split(',') if rent[8] else []
        if photos:
            media_group = [InputMediaPhoto(media=photo) for photo in photos if all(c.isalnum() or c in '-_' for c in photo)]
            try:
                await message.answer_media_group(media_group)
            except Exception as e:
                await message.answer(f"Ошибка при загрузке фото: {e}")
        await message.answer(
            text=new_caption,
            reply_markup=kb.moderate
        )
        await state.update_data(current_index=current_index + 1)
    else:
        await message.answer("Нет объявлений для модерации.", reply_markup=kb.main)

@router.callback_query(F.data == "delete")
async def delete_rent(callback_query: CallbackQuery, state: FSMContext):
            data = await state.get_data()
            rent_data = data['rent_data']
            current_index = data['current_index']
            rent = rent_data[current_index - 1]
            
            async with aiosqlite.connect('bot_database.db') as db:
                await db.execute('DELETE FROM rent WHERE rowid = ?', (rent[0],))
                await db.execute('DELETE FROM favorites WHERE town = ? AND district = ? AND type = ? AND area = ? AND rooms = ? AND price = ? AND description = ? AND photo = ?', 
                                 (rent[1], rent[2], rent[3], rent[4], rent[5], rent[6], rent[7], rent[8]))
                await db.commit()
            
            await callback_query.answer("Объявление удалено.")
            await show_next_moderate(callback_query.message, state)

@router.callback_query(F.data == "next_moderate")
async def next_moderate(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    rent_data = data.get('rent_data', [])
    current_index = data.get('current_index', 0)
    
    if current_index < len(rent_data):
        await show_next_moderate(callback_query.message, state)
    else:
        await callback_query.answer("Это последнее объявление.", show_alert=True)

@router.callback_query(F.data == "previous_moderate")
async def previous_moderate(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_index = data.get('current_index')
    if current_index is not None and current_index > 1:
        await state.update_data(current_index=current_index - 2)
        await show_next_moderate(callback_query.message, state)
    else:
        await callback_query.answer("Это первое объявление.", show_alert=True)

#Мои объявления

@router.message(F.text == "📢 Мои Объявления")
async def personal_account(message: Message, state: FSMContext):
                async with aiosqlite.connect('bot_database.db') as db:
                    cursor = await db.execute('SELECT town, district, area, type, rooms, price, description, photo FROM rent WHERE telegram_id = ?', (message.from_user.id,))
                    rent_data = await cursor.fetchall()
                    if rent_data:
                        await state.update_data(rent_data=rent_data, current_index=0)
                        await show_next_rent(message, state)
                    else:
                        await message.answer("У вас нет объявлений.", reply_markup=kb.main)

async def show_next_rent(message: Message, state: FSMContext):
    data = await state.get_data()
    rent_data = data.get('rent_data', [])
    current_index = data['current_index']
    
    if current_index < len(rent_data):
        rent = rent_data[current_index]
        photos = rent[7].split(',') if rent[7] else []
        if photos:
            media_group = [InputMediaPhoto(media=photo) for photo in photos]
            try:
                await message.answer_media_group(media_group)
                await message.answer(
                    f"Город: {rent[0]}\nРайон: {rent[1]}\nТип Жилья: {rent[3]}\nПлощадь: {rent[2]}\nКомнаты: {rent[4]}\nЦена: {rent[5]}\nОписание: {rent[6]}",
                    reply_markup=kb.next
                )
            except Exception as e:
                await message.answer(f"Ошибка при загрузке фото: {e}")
        else:
            await message.answer(
                f"Город: {rent[0]}\nРайон: {rent[1]}\nТип Жилья: {rent[3]}\nПлощадь: {rent[2]}\nКомнаты: {rent[4]}\nЦена: {rent[5]}\nОписание: {rent[6]}",
                reply_markup=kb.next
            )
        await state.update_data(current_index=current_index + 1)
    else:
        await message.answer("Это были все ваши объявления.", reply_markup=kb.main)
        await state.clear()

@router.callback_query(F.data == "next")
async def next_rent(callback_query: CallbackQuery, state: FSMContext):
                await callback_query.answer()
                await show_next_rent(callback_query.message, state)


