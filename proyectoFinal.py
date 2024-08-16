from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup 
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import random
import unicodedata 
import pokebase as pb
import os
TOKEN = os.getenv('TELEGRAM_TOKEN')


products = [ 
    { 
        'name': 'Manzana', 
        'description': 'Roja o verde', 
        'price': '$10.00', 
        'rating': '★ ★ ★ ★ ', 
        'comments': 'Muy rica la manzana', 
        'image_url': 'https://plus.unsplash.com/premium_photo-1668772704261-b11d89a92bad?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8YXBwbGV8ZW58MHx8MHx8fDA%3D' 
    }, 
    { 
        'name': 'Pan dulce', 
        'description': 'Pan envuelto y relleno', 
        'rating': '★ ★ ★ ★ ★ ', 
        'price': '$20.00', 
        'comments':'Me gusta mucho', 
        'image_url': 'https://plus.unsplash.com/premium_photo-1675788939191-713c2abf3da6?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8YnJlYWR8ZW58MHx8MHx8fDA%3D' 
    }, 
     { 
        'name': 'Perro', 
        'description': 'De raza', 
        'rating': '★ ★ ★  ', 
        'price': '$400.00', 
        'comments':'Muy bonito perro', 
        'image_url': 'https://plus.unsplash.com/premium_photo-1676390051589-bead49b416a6?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8ZG9nfGVufDB8fDB8fHww' 
    }, 
     { 
        'name': 'Gato', 
        'description': 'Recien nacido', 
        'rating': '★', 
        'price': '$20.00', 
        'comments':'Muy bonito gato', 
        'image_url': 'https://images.unsplash.com/photo-1526336024174-e58f5cdd8e13?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Y2F0fGVufDB8fDB8fHww' 
    } 
] 

knowledge_base_general_culture = { 
    '¿El cielo es de color?': ['azul', 'celeste', 'cielo azul'],
    'Normalmente, ¿de qué color pintas una casa?': ['blanco','amarillo','verde'],
    'Dame el nombre de algún continente.':['africa', 'america', 'europa', 'asia','oceania'],
    'Dame el nombre de un océano.': ['pacifico', 'indico', 'atlantico', 'artico', 'antartico'],
    '¿Cuál es el planeta más cercano al Sol?': ['mercurio'] 
} 

trivia_questions_by_mood = {
    'enojado': {
        'questions': [
            "¿Cuál es el estado de ánimo más común cuando alguien está frustrado?",
            "¿Qué actividad puede ayudar a calmar la ira?",
            "¿Cuál es una forma de manejar el estrés relacionado con la ira?"
        ],
        'options': [
            ['Triste', 'Feliz', 'Enojado'],
            ['Hacer ejercicio', 'Ver televisión', 'Dormir'],
            ['Hablar con alguien', 'Gritar', 'Ignorar el problema']
        ],
        'correct_answer': [
            'Enojado',
            'Hacer ejercicio',
            'Hablar con alguien'
        ]
    },
    'triste': {
        'questions': [
            "¿Cuál es una buena manera de mejorar el ánimo cuando te sientes triste?",
            "¿Qué tipo de música puede ayudar a levantar el ánimo?",
            "¿Cuál de las siguientes actividades es recomendable para alguien que se siente deprimido?"
        ],
        'options': [
            ['Salir con amigos', 'Ver una película triste', 'Quedarte solo'],
            ['Música alegre', 'Música triste', 'Música instrumental'],
            ['Hacer ejercicio', 'Evitar el contacto social', 'No hacer nada']
        ],
        'correct_answer': [
            'Salir con amigos',
            'Música alegre',
            'Hacer ejercicio'
        ]
    },
    'feliz': {
        'questions': [
            "¿Qué actividad es excelente para compartir cuando te sientes feliz?",
            "¿Cuál es una forma de extender la felicidad a los demás?",
            "¿Qué tipo de actividad puede reforzar tu felicidad?"
        ],
        'options': [
            ['Salir a comer', 'Quedarte en casa', 'Leer un libro'],
            ['Compartir buenas noticias', 'Mantenerse en silencio', 'Dejar a los demás en paz'],
            ['Participar en eventos sociales', 'Trabajar más horas', 'Ver televisión solo']
        ],
        'correct_answer': [
            'Salir a comer',
            'Compartir buenas noticias',
            'Participar en eventos sociales'
        ]
    }
}


def remove_accents(text: str) -> str:
    """Remove accents from a given text."""
    text = unicodedata.normalize('NFKD', text)
    return text.encode('ASCII', 'ignore').decode('ASCII').lower()


async def inicio(chat_id: int, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /inicio is issued."""
    welcome_message = "Bienvenido, selecciona una de las opciones para interactuar:"
    keyboard = [
    [InlineKeyboardButton("Opción 1. Estado de ánimo", callback_data='1')],
    [InlineKeyboardButton("Opción 2. Chatear con el bot y cultura general", callback_data='2')],
    [InlineKeyboardButton("Opción 3. Ventas de productos", callback_data='3')],
    [InlineKeyboardButton("Opción 4. Buscar pokemons", callback_data='4')],
    [InlineKeyboardButton("Opción 5. Descargar código o salir", callback_data='5')]
    ]


    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(chat_id=chat_id, text=welcome_message, reply_markup=reply_markup)


user_data = {}

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    response = 'Opción no reconocida'

    if query.data == '1':
        keyboard = [
            [InlineKeyboardButton("Evaluar estado de ánimo", callback_data='1.1')],
            [InlineKeyboardButton("Trivia", callback_data='1.2')],
            [InlineKeyboardButton("Regresar al menú anterior", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Seleccionaste la opción 1. Selecciona lo que deseas hacer", reply_markup=reply_markup)
        return
    elif query.data == '1.1':
        message = 'Seleccionaste Evaluar estado de ánimo. Selecciona tu estado de ánimo'
        keyboard = [
            [InlineKeyboardButton("Enojado", callback_data='1.1.1')],
            [InlineKeyboardButton("Triste", callback_data='1.1.2')],
            [InlineKeyboardButton("Feliz", callback_data='1.1.3')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=message, reply_markup=reply_markup)
        return
    elif query.data == '1.1.1':
        user_data[query.from_user.id] = {'mood': 'enojado'}
        message = 'No te enojes, después se te va a pasar. \n ¿Deseas volver a ingresar tu estado de ánimo?'
        keyboard = [
            [InlineKeyboardButton("Si", callback_data='1.1')],
            [InlineKeyboardButton("No", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=message, reply_markup=reply_markup)
        return
    elif query.data == '1.1.2':
        user_data[query.from_user.id] = {'mood': 'triste'}
        message = 'No seas chillón, anímate.\n ¿Deseas volver a ingresar tu estado de ánimo?'
        keyboard = [
            [InlineKeyboardButton("Si", callback_data='1.1')],
            [InlineKeyboardButton("No", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=message, reply_markup=reply_markup)
        return
    elif query.data == '1.1.3':
        user_data[query.from_user.id] = {'mood': 'feliz'}
        message = 'Eale, yo también estoy feliz.\n ¿Deseas volver a ingresar tu estado de ánimo?'
        keyboard = [
            [InlineKeyboardButton("Si", callback_data='1.1')],
            [InlineKeyboardButton("No", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=message, reply_markup=reply_markup)
        return
    elif query.data == '1.2':
        user_id = query.from_user.id
        mood = user_data.get(user_id, {}).get('mood', None)

        if not mood:
            message = 'Primero necesitas evaluar tu estado de ánimo. \n ¿Deseas ir a evaluar?'
            keyboard = [
            [InlineKeyboardButton("Si", callback_data='1.1')],
            [InlineKeyboardButton("No", callback_data='main_menu')]
        ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text=message, reply_markup=reply_markup)
            return

        await trivia_questions(update, context, mood)
        return
    

    elif query.data == '2':
        message = 'Seleccionaste la opción 2. Selecciona lo que deseas hacer.'
        keyboard = [
            [InlineKeyboardButton("Conversar conmigo", callback_data='2.1')],
            [InlineKeyboardButton("Una pregunta de cultura general", callback_data='2.2')],
            [InlineKeyboardButton("Regresar al menú anterior", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=message, reply_markup=reply_markup)
        return
    elif query.data == '2.1':
        user_id = query.from_user.id
        user_data[user_id] = {'state': 'asking_name'}
        await query.edit_message_text("¿Cuál es tu nombre?")
        return
    elif query.data == '2.2':
        await ask_random_question(update, context)
        return
    

    elif query.data == '3':
        user_id = query.from_user.id
        user_data[user_id] = {'awaiting_products_list': True}
        await query.edit_message_text(text="Lista de productos disponibles:\n")
        for product in products:
            await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=product['image_url'],
            caption=(
                f"Nombre: {product['name']}\n"
                f"Descripción: {product['description']}\n"
                f"Precio: {product['price']}\n"
                f"Rating: {product['rating']}\n"
                f"Comentarios: {product['comments']}\n\n"
            )
        )
    
        await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="Escribe los nombres de los productos que deseas comprar, separados por coma."
        )
        return
    

    elif query.data == '4':
        user_id = query.from_user.id
        user_data[user_id] = {'awaiting_pokemon_name': True}
        await query.edit_message_text(text="Seleccionaste poke api. Escribe el nombre de un Pokémon.")
        return

    elif query.data == '5':
        message = 'Seleccionaste la opción 5. Selecciona lo que deseas hacer.'
        keyboard = [
            [InlineKeyboardButton("Ver link de descarga de código", callback_data='5.1')],
            [InlineKeyboardButton("Salir del bot", callback_data='5.2')],
            [InlineKeyboardButton("Regresar al menú anterior", callback_data='main_menu')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=message, reply_markup=reply_markup)
        return
    elif query.data == '5.1':
        message ='Aquí esta el link de descarga del código: \n https://1drv.ms/u/c/daf3fc71ed3dd3d8/EZMCnwrfIXdIrqoSmElvXgIBCOhG2Jlw39gJcETIMibCrQ?e=PcBkjM'
        await query.edit_message_text(text=message)
        chat_id = update.message.chat.id
        await inicio(chat_id, context)
        return
    elif query.data == '5.2':
        await stop(query, context)
        return
            

    elif query.data == 'main_menu':
        chat_id = query.message.chat.id
        await inicio(chat_id, context)
        return
    
    await query.edit_message_text(text=response)



async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stop the bot."""
    await update.message.reply_text('Gracias por usar rodrigoBot.')
    context.application.stop()


async def ask_random_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ask a random general culture question."""
    query = update.callback_query
    user_id = query.from_user.id

    question, answers = random.choice(list(knowledge_base_general_culture.items()))
    user_data[user_id] = {'question': question, 'correct_answers': answers}

    response = f"Pregunta: {question}"
    await context.bot.send_message(chat_id=user_id, text=response)


async def trivia_questions(update: Update, context: ContextTypes.DEFAULT_TYPE, mood: str) -> None:
    """Handle the trivia questions based on mood."""
    query = update.callback_query
    user_id = query.from_user.id
    trivia = trivia_questions_by_mood[mood]

    user_data[user_id]['trivia'] = {'current_question': 0, 'questions': trivia['questions'], 'options': trivia['options'], 'correct_answer': trivia['correct_answer']}

    question_text = trivia['questions'][0]
    option_text = '\n'.join(f"{i+1}. {option}" for i, option in enumerate(trivia['options'][0]))

    response = f"Trivia: {question_text}\n{option_text}\nDebes escribir la respuesta sin el número."
    await context.bot.send_message(chat_id=user_id, text=response)  

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user's answer to a question."""
    user_id = update.message.from_user.id
    user_text = update.message.text.strip()
    user_info = user_data.get(user_id, {})

    if 'question' in user_info:
        correct_answers = [remove_accents(ans) for ans in user_info['correct_answers']]
        normalized_user_text = remove_accents(user_text)

        if normalized_user_text in correct_answers:
            await update.message.reply_text('¡Correcto!')

            keyboard = [
                [InlineKeyboardButton("Si", callback_data='2.2')],
                [InlineKeyboardButton("No", callback_data='main_menu')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                "¿Te gustaría responder otra pregunta? Podría ser que tengas suerte y sea la misma o bien sea diferente.",
                reply_markup=reply_markup
            )
            del user_data[user_id]
        else:
            await update.message.reply_text('Incorrecto, inténtalo de nuevo.')

    

    elif 'trivia' in user_info:
        trivia = user_info['trivia']
        current_question = trivia['current_question']
        correct_answer = trivia['correct_answer'][current_question]

        if user_text.lower() == correct_answer.lower():
            await update.message.reply_text('¡Correcto!')
            trivia['current_question'] += 1

            if trivia['current_question'] < len(trivia['questions']):
                question_text = trivia['questions'][trivia['current_question']]
                option_text = '\n'.join(f"{i+1}. {option}" for i, option in enumerate(
                    trivia['options'][trivia['current_question']]))

                response = f"Trivia: {question_text}\n{option_text}\nDebes escribir la respuesta sin el número."
                await update.message.reply_text(response)
            else:
                await update.message.reply_text('¡Has completado todas las preguntas de trivia!')
                chat_id = update.message.chat.id
                del user_data[user_id]
                await inicio(chat_id, context)
                return
        else:
            await update.message.reply_text(f'Incorrecto. La respuesta correcta es: {correct_answer}')
    elif 'awaiting_products_list' in user_info:
        product_names = [name.strip().lower() for name in user_text.split(',')]
        valid_products = [product['name'].lower() for product in products]
        if all(name in valid_products for name in product_names):
            total = 0.0

            for product in products:
                if product['name'].lower() in product_names:
                    price = float(product['price'].replace('$', '').replace(',', ''))
                    total += price

            response = f"Total a pagar: ${total:.2f}. Gracias por tu compra."
            await update.message.reply_text(response)
            del user_data[user_id]
            chat_id = update.message.chat.id
            await inicio(chat_id, context)
            return
        else:
            await update.message.reply_text("Uno de los productos ingresados no está en la lista, inténtalo de nuevo.")
            return
        
    elif 'awaiting_pokemon_name' in user_info:
        pokemon_name = user_text.strip().lower()
        user_data[user_id].pop('awaiting_pokemon_name', None)

        try:
            pokemon = pb.pokemon(pokemon_name)
            image_url = pb.SpriteResource('pokemon', pokemon.id).url
            await update.message.reply_photo(
                photo=image_url,
                caption=f"¡Aquí está la imagen de {pokemon_name.title()}!"
            )
            keyboard = [
                [InlineKeyboardButton("Sí", callback_data='4')],
                [InlineKeyboardButton("No", callback_data='main_menu')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "¿Deseas intentarlo de nuevo?",
                reply_markup=reply_markup
            )
        except Exception as e:
            keyboard = [
                [InlineKeyboardButton("Sí", callback_data='4')],
                [InlineKeyboardButton("No", callback_data='main_menu')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "Pokémon no encontrado, ¿deseas intentarlo de nuevo?",
                reply_markup=reply_markup
            )
        return
        
    else:
        if user_info.get('state') == 'asking_name':
            user_data[user_id]['answer'] = user_text
            user_data[user_id]['state'] = 'asking_age'
            await update.message.reply_text(f"Hola {user_text}, ¿cuántos años tienes?")
        elif user_info.get('state') == 'asking_age':
            user_data[user_id]['answer'] = user_text
            user_data[user_id]['state'] = 'asking_phone'
            await update.message.reply_text(f"Tienes {user_text} años, ¿cuál es tu número telefónico?")
        elif user_info.get('state') == 'asking_phone':
            user_data[user_id]['answer'] = user_text
            user_data[user_id]['state'] = 'asking_address'
            await update.message.reply_text(f"Tu número es {user_text}. ¿Cual es tu dirección?")
        elif user_info.get('state') == 'asking_address':
            user_data[user_id]['answer'] = user_text
            user_data[user_id]['state'] = 'completed'
            await update.message.reply_text(f"Tu dirección es {user_text}. \n Gracias por conversar conmigo.")
            del user_data[user_id]
            chat_id = update.message.chat.id
            await inicio(chat_id, context)
            return

def handle_inicio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /inicio command."""
    chat_id = update.message.chat_id
    return inicio(chat_id, context)

def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('inicio', handle_inicio))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer))
    application.run_polling()

if __name__ == '__main__':
    main()
