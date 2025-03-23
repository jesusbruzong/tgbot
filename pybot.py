#Modulos
import telebot
from telebot.types import ReplyKeyboardMarkup
import time
import threading
from config import *
from telebot.types import ForceReply
from telebot import types
 
"""
TENER EN CUENTA

LAS VARIABLES telegram_token y chat_id SE ENCUENTRAN EN EL ARCHIVO config.py en ese mismo archivo tendras que cambiar
los valores por los tuyos propios, en este caso son:

telegram_token: Esta variable se encarga de recoger el valor del token de tu bot (su identificador)

chat_id: Esta variable se encarga de almacenar el ID del chat del administrador al que le llegaran los datos de las altas
(correos, etc...)

"""
 
####################################################  
 
"""CREACION DEL OBJETO BOT E INSTANCIADO EN TELEGRAM"""

#instanciar el bot en tg
bot = telebot.TeleBot(telegram_token,parse_mode=None)

####################################################

#Variable que guarda los correos para la solicitud de demos

correos_demo = {}

####################################################

"""INICIO DE LOS COMANDOS"""

#Comando start
@bot.message_handler(commands=["start"])
def send_welcome(message):
    #Da la bienvenida al usuario del bot
    bot.reply_to(message, ("Servicio de asistencia del servicio Plex Macflys"), reply_markup = markup)
    
#responde al comando /demo       
@bot.message_handler(commands=["demo"])
def solicitar_demo(message):
    #pregunta el correo para solicitar la demo
    correos_demo[message.chat.id] = {}
    correos_demo[message.chat.id]["Correos"] = message.text
    markup = ForceReply()
    bot.send_message(message.chat.id, "Bienvenido, para solicitar la demo, debe registrarse en https://www.plex.tv una vez registrado nos deberá enviar mediante el siguiente mensaje el correo electrónico con el que se ha registrado.")
    msg = bot.send_message(message.chat.id, f'Indiquenos el correo utilizado para el registro del mensaje anterior \n Asegurese de que el correo es correcto antes de enviarlo para evitar confusiones.', reply_markup=markup)
    bot.register_next_step_handler(msg, preguntar_correo)
    

#responde al comando /pagos
@bot.message_handler(commands=["pagos"])
def send_pay(message):
    #Da los metodos de pago al usuario del bot
    bot.reply_to(message, ("Los unicos metodos de pago, soportados son; PAYPAL & BIZUM"))
    
#responde al comando /precios
@bot.message_handler(commands=["precios"])
def send_price(message):
    #Da los precios del servicio al usuario del bot
    bot.reply_to(message, ("TARIFA ANUAL: 1 dispositivo = 60€"))

#responde al comando /ayuda
@bot.message_handler(commands=["ayuda"])
def send_help(message):
    #Da los precios del servicio al usuario del bot
    bot.reply_to(message, ("Si necesitas ayuda contactar con @xsmkez"))
    
#responde al comando /condiciones
@bot.message_handler(commands=["condiciones"])
def send_conditions(message):
    #Da los precios del servicio al usuario del bot
    bot.reply_to(message, (condiciones))

       
#responde al comando /horarios
@bot.message_handler(commands=["horarios"])
def send_time(message):
    bot.reply_to(message, ("""
⏰HORARIO INVIERNO⏰

🔷 L - V : 10:00 - 13:30 y 17:00 - 21:00
🔶 S  : 10:00 - 13:30
⛔️ D y FESTIVOS: ❌ """))        


#########################################################


#Botones
markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, input_field_placeholder= "Pulsa un botón")
boton_op_1 = types.KeyboardButton('🆘Ayuda🆘')
boton_op_2 = types.KeyboardButton('📺Solicitar Demo📹')
boton_op_3 = types.KeyboardButton('💲Métodos de pago💳')
boton_op_4 = types.KeyboardButton('💳Precios💶')
boton_op_5 = types.KeyboardButton('📝Condiciones📝')
boton_op_6 = types.KeyboardButton('⏰Horarios⏰')

#cuadricula de botones
markup.row(boton_op_1,boton_op_2,boton_op_3 )
markup.row(boton_op_4,boton_op_5,boton_op_6)

#forzado de emojis




#Respuesta a los mensajes (no comandos) (y respuesta a los botones sin la / de comando)
@bot.message_handler(content_types=["text"])
def Mensajes_De_texto(message):
    #Gestiona los mensajes de texto recibidos
    #respuesta para los mensajes que no son comandos (no tienen /) y que no estan registrados para funcionar
    if message.text.startswith("/"):
        bot.send_message(message.chat.id, "introduce un comando válido")
    #respuesta para el boton condiciones con emoticonos
    elif message.text == "📝Condiciones📝":
        bot.reply_to(message, (condiciones))
    #respuesta para el boton ayuda con emoticonos
    elif message.text == "🆘Ayuda🆘":
        bot.reply_to(message, ("Si necesitas ayuda contactar con @Macflys"))
    #respuesta para el boton horarios sin emoticonos
    elif message.text == "⏰Horarios⏰":    
        bot.reply_to(message, ("""
        ⏰HORARIO INVIERNO⏰

        🔷 L - V : 10:00 - 13:30 y 17:00 - 21:00
        🔶 S  : 10:00 - 13:30
        ⛔️ D y FESTIVOS: ❌ """))       
    #respuesta para el boton metodos de pago sin emoticonos
    elif message.text == "💲Métodos de pago💳":
            bot.reply_to(message, ("Los unicos metodos de pago, soportados son; PAYPAL & BIZUM"))
    #respuesta para el boton solicitar demo sin emoticonos
    elif message.text == "📺Solicitar Demo📹":
            solicitar_demo(message)
    #respuesta para el boton precios sin emoticonos
    elif message.text == "💳Precios💶":
            bot.reply_to(message, ("TARIFA ANUAL: 1 dispositivo = 60€"))
    else:
        bot.send_message(message.chat.id, """Bienvenido a DEMO los comandos disponibles son:
                                            \n/start \n/ayuda \n/demo \n/pagos \n/precios \n/condiciones \n/horarios""", reply_markup= markup)
        
 
def preguntar_correo(message):
    #pregunta el correo del usuario
    correo = message.text 
    bot.send_message(chat_id, "se ha registrado un nuevo correo electrónico: " + correo, reply_markup=markup)
    bot.send_message(message.chat.id, "Su solicitud ha sido puesta en cola, revise su bandeja de entrada para aceptar la invitacion. \nDispondrá de 24 horas para aceptarla.")


"""FIN DE LOS COMANDOS"""    
    
#######################################################

"""COMPROBADOR DE MENSAJES INFINITO"""

def recibir_mensajes():
    #Bucle infinito que comprueba si hay nuevos mensajes en el bot
    bot.infinity_polling()    
    
"""Muestra por consola los datos introducidos por el usuario, para las altas de las demos"""
    
def guardar_datos_usuarios(message):
    texto = "Correo introducido:\n"
    texto+= f'<code>Correo...:</code> {correos_demo[message.chat.id]["correo"]}\n'
    
########################################################

"""FUNCION PRINCIPAL DEL BOT"""

#MAIN
if __name__ == "__main__":
    print("iniciando el bot")
    #ponemos el comprobador de mensajes entrantes en segundo plano
    hilo_bot = threading.Thread(name="telegram_hilo_bot", target=recibir_mensajes)
    hilo_bot.start()
    print("Porfavor no apagues el dispositivo, ni cierres esta ventana . . . 100%")
    print("""Este bot ha sido desarrollado con amor (y mucho estrés)
          por Jesus Bruzon Guerrero at practica's company
          
          pd: No borreis este mensaje, que es mi legado :( """)
    print(correos_demo)
"""FIN DEL SCRIPT""" 


""" 
ERRORES: 
    
    1. La botonera esta hecha pero solo responde sin dar formato a los botones, es decir
    el boton tiene que ser /ayuda por ejemplo. --> solucionar para poder darle formato a los botones.
    
    ENCONTRAR CODIGOS UTF 8 DE LOS EMOJIS
      
    SOLUCIONADO:
    1. :)
    
"""
