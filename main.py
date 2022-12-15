import os
import discord
import time
import ast
import requests


from discord.ext import commands
from running import *

from discord.utils import get
from translate import Translator

print("hi")
print("test2")
'''
IMPORTANT:::::

#1: IF GIVEN THE OPTION OF "CHOOSE MY CHANGES" OR "CHOOSE SERVER CHANGES", CHOOSE "CHOOSE SERVER CHANGES", OR THE COUNTING PROGRESS IS GONNA GET DELETED!!!!!!!!

#2: "from translate import Translator" requires you typing "$pip install translate" inside of the shell in order to work.

#3: "from running import *" is needed for the running() function below to work. Essentially, running() creates an HTTP server that constantly keeps the bot alive.
'''


debug_mode = "off"
client = commands.Bot(command_prefix="",intents=discord.Intents.all())
currencybot = commands.Bot(command_prefix="p:",intents=discord.Intents.all())

# Runs when the bot starts.
@client.event
async def on_ready():
  # Sets all of the global variables to their base value.
    global countlist
    global previous_person
    global messages
    global globalvictorymessage
    global Data_storage
    global pumpcoin_dict
    Data_storage = {}
    countlist = {}
    previous_person = {}
    messages = {}
    pumpcoin_dict = {}
    globalvictorymessage = ""
    # This is where the bot compiles data. 
    # I have a special discord server that the bot posts counting data to, as a dictionary.
    # Every time somebody counts, the bot will post that updated information onto the specialized discord server.
    # Since I use uptimerobot to keep the bot running, this code reads the info stored in that discord server in order for the counting data to not be lost once the code reloads.

    print("Bot is still compiling data, please wait.......")
    
    counting_channel = client.get_channel(1008040131879522356)
    pumpcoin_channel = client.get_channel(1008040158597234758)
  
    # Credits: leo848, https://stackoverflow.com/questions/64080277/how-to-get-the-most-recent-message-of-a-channel-in-discord-py#
    # Reads the most recent message in a discord chat channel. This is used to extract the counting and pumpcoin data.
    
    Counting_data = await counting_channel.fetch_message(1008041694261936218)
    pumpcoin_dict = await pumpcoin_channel.fetch_message(1008041694706548737)
    # I use ast.literal_eval to turn the data(stored as a string) into an actual dictionary.
    print(Counting_data)
    Counting_data = ast.literal_eval(Counting_data.content)
    pumpcoin_dict = ast.literal_eval(pumpcoin_dict.content)
  
    # Extracts the data from the counting_data dict, which has subdictionaries inside of it.
    countlist = Counting_data["countlist"]
    previous_person = Counting_data["previous_person"]
    # Specific server-wide counting messages.
    messages = Counting_data["messages"]
    # The global victory message stores the message that every server will see once they count.
    globalvictorymessage = Counting_data["globalvictorymessage"]
    print("Bot has finished compiling data. You can start counting now!")

    await client.change_presence(activity=discord.Game('with other cats like me!'))


@client.event
async def on_message(message):
    # Global variables for use are here:
    global countlist
    global previous_person
    global messages
    global globalvictorymessage
    global Data_storage
    global Temp_storage
    global pumpcoin_dict



    # This is where the bot's currency functions reside!!!!!!
    lowercasemessage = message.content.lower()

    if message.content.startswith("p&") or message.content.startswith("c&") or message.content.startswith("currency:") or message.content.startswith("pumpkin:"):

        
        # Reduces pumpcoins of a user. How to run: p&deduct @user,amount. Admin command: Only person that can run this command is me(@DanielRocksUrMom). 
        if ("deduct" in message.content.lower() or "reduce" in message.content.lower()) and message.author.id == 614549755342880778:
            important_content = message.content.split()
            important_content = "".join(important_content[1:])
            while " " in important_content:
                temp_index = important_content.find(" ")
                important_content = important_content[:temp_index] + important_content[temp_index + 1:]
            print(important_content)
            comma_index = important_content.find(",")
            amount_to_deduct = int(important_content[comma_index + 1:])
            user = important_content[:comma_index]
            user = user[2:-1]
            user = await client.fetch_user(user)
            print(user)
            try:
                pumpcoin_dict[user.name] -= amount_to_deduct
                await message.channel.send(str(amount_to_deduct) +" pumpcoins have been deducted from " + str(user.name))
            except:
                await message.channel.send("User does not have a pumpkincoin value yet, or an error could have occured. You could have forgot to @ the user, or they may not have a pumpcoin value yet.")


              

      # Gives user pumpcoins. How to run: p&add @user, amount. Admin command: Only person that can run this command is me(@DanielRocksUrMom)      
        elif ("add" in message.content.lower() or "increase" in message.content.lower() or "award" in message.content.lower() or "give" in message.content.lower()) and message.author.id == 614549755342880778:
            
            important_content = message.content.split()
            important_content = "".join(important_content[1:])
            while " " in important_content:
                temp_index = important_content.find(" ")
                important_content = important_content[:temp_index] + important_content[temp_index + 1:]
            print(important_content)
            comma_index = important_content.find(",")
            amount_to_deduct = int(important_content[comma_index + 1:])
            user = important_content[:comma_index]
            user = user[2:-1]
            user = await client.fetch_user(user)
            print(user)
            try:
                pumpcoin_dict[user.name] += amount_to_deduct
            except:
                pumpcoin_dict[user.name] = 0
                pumpcoin_dict[user.name] += amount_to_deduct
            
            await message.channel.send(str(amount_to_deduct) + " pumpcoins have been added to" +str(user.name))


          
                
        # Gifts user pumpcoins, which takes out some of your pumpcoins to give to the appropriate user.
        elif "gift" in message.content.lower():
            await message.channel.send("gifting functionality coming soon!")
        elif "shop" in message.content.lower() or "spend" in message.content.lower():
          embed = discord.Embed(title="The pumpcoin store", description="Welcome to the pumpcoin store, where you can spend your pumpcoins for special rewards. Here is a list on what you can buy:", color=0xf1c40f)
          embed.add_field(name="1. Channels", value="Channels allow you to specify custom counting conditions. For example, you can enable counting by a different number(like 69), count by roman numerals, by english words, and even by chinese! In order to do that, type p&add_channel in order to create a new channel with custom counting conditions!", inline=False)
          await message.channel.send(embed=embed)


        if "leaderboard" in message.content.lower() or "rankings" in message.content.lower():
            # Sorts the dict by the largest value. Got it from stackoverflow lol
            sorted_dict = dict(sorted(pumpcoin_dict.items(), key=lambda item: item[1]))
            sorted_dict = dict(reversed(list(sorted_dict.items())))
            sorted_dict = list(str(sorted_dict))
            while "{" in sorted_dict:
                sorted_dict.remove("{")
            while "}" in sorted_dict:
                sorted_dict.remove("}")
            while "'" in sorted_dict:
                sorted_dict.remove("'")
            ordering_var = 2
            while "," in sorted_dict:
                temp_comma_index = sorted_dict.index(",")
                sorted_dict[temp_comma_index] = "\n" + str(ordering_var) + ". "
                ordering_var += 1
            # The ```yaml is to make it in an embed format
            sorted_dict = """```yaml\nPUMPCOIN LEADERBOARD:\n1.  """ + str("".join(sorted_dict)) + """```"""
            await message.channel.send(sorted_dict)
        elif "mypumpcoin" in message.content.lower() or "my_pumpcoin" in message.content.lower():
            await message.channel.send("You currently have "+str(pumpcoin_dict[message.author.name])+" pumpcoins. To spend them, type p&spend or p&shop!")


          
        

    # These are the settings changers. They set the messages that will be played once a user counts correctly. The regular victory message is per-server only, while the global victory message plays on all servers this bot is on.

    if "victorymessage:" in lowercasemessage or "victory message:" in lowercasemessage:
        if ("globalvictorymessage:" in lowercasemessage
                or "global victory message" in lowercasemessage) == False:
            nessecary_content = message.content[message.content.find(":") + 1:]
            messages[message.channel.guild.name] = nessecary_content
            await message.channel.send(
                "Meow! Server-only victory message has been set to:" +
                str(globalvictorymessage) +
                ". If you want your victory message to appear on all servers, type **globalvictorymessage: *your message here* **"
            )

    if "clearvictorymessage" in lowercasemessage or "clear victory message" in lowercasemessage or "resetvictorymessage" in lowercasemessage or "reset victory message" in lowercasemessage:
        messages[message.channel.guild.name] = ""
        await message.channel.send(
            "Meow. Server-side victory message has been reset to nothing! There may be a global victory message left over, to reset that, type **clearvictorymessage**. "
        )

    if "globalvictorymessage:" in lowercasemessage or "global victory message" in lowercasemessage:
        globalvictorymessage = message.content[message.content.find(":") + 1:]
        await message.channel.send(
            "Meow! Global victory message has been set to:" +
            str(globalvictorymessage) +
            ". If you want your victory message to appear only on your server, type **victorymessage: *your message here* **"
        )

    if "clearglobalvictorymessage" in lowercasemessage or "clear global victory message" in lowercasemessage or "resetglobalvictorymessage" in lowercasemessage or "reset global victory message" in lowercasemessage:
        globalvictorymessage = ""
        await message.channel.send(
            "Meow. Global victory message has been reset to nothing! To reset your server-only victory message, type **clearvictorymessage**. "
        )

    # The counting procedure is here.
    # This detects whether "count" is in the channel name.
    if "count" in message.channel.name and message.author.bot == False and message.channel.name != "counting-spamathon":
        # Detects whether an item is not a key in the specified dictionary.
        def not_in_dict(key, dict):
            try:
                randomvariable69 = dict[key]
                return False
            except KeyError:
                return True

        mychannel = message.channel

        # Checks to see if a channel has been marked inside of my server
        def guildchecker():
            try:
                if not (mychannel.guild.name in countlist):
                    return True
                else:
                    return False
            except:
                return False

        # Uses guildchecker() to check if the channel is has been marked yet, then splits it by the dashes, into count, by, and (a number). It then detects the number
        if guildchecker():
            temp = mychannel.name.split("-")
            if "by" in temp:
                count_by_num = int(temp[temp.index("by") + 1])
            else:
                count_by_num = 1
            countlist[mychannel.guild.name] = {}
            previous_person[mychannel.guild.name] = {}

        # Detects if a channel is not inside of the dictionary inside of: the dictionary that has the server's key. Does this for both countlist and previous_person.
        if not_in_dict(mychannel.name,countlist[mychannel.guild.name]) and not_in_dict(mychannel.name,previous_person[mychannel.guild.name]):
            temp = mychannel.name.split("-")
            if "by" in temp:
                hi = int(temp[temp.index("by") + 1])
            else:
                hi = 1
            countlist[mychannel.guild.name][mychannel.name] = hi
            previous_person[mychannel.guild.name][mychannel.name] = -1

        if mychannel.guild.name in countlist and mychannel.name in countlist[mychannel.guild.name]:
            # These are the fundamental functions which will be used later in the program.
            # This detects whether the content inputed can be transformed into an integer of some kind.
            def is_intable(content):
                try:
                    lol = int(content)
                    return True
                except:
                    return False

            # This detects whether the inputted message has a number inside of it.

            def has_number(message):
                listmessage = list(message)
                for i in range(len(message)):
                    if is_intable(listmessage[i]):
                        return True
                return False

            # The same as is_intable, but for floats(like decimal numbers)
            def is_floatable(string):
                if string == " ":
                    return False
                try:
                    variable = float(string)
                    return True
                except ValueError:
                    return False

            # Detects whether a string is an expression/operation. I Split it into 2 if statements to make it more readable.
            def is_operation(string):
                if string == "+" or string == "-" or string == "*":
                    return True
                elif string == "^" or string == "/":
                    return True
                else:
                    return False

            # Properly organizes and combines parts of the expression to allow solve_string to work. Only used as a base operation for the solve_string() function.
            def organize_expression(operation_string):
                operation_list = []
                int_storage_var = ""
                # This for loop divides the operation string into the numbers and operations
                # Operations are like *, /, +, -, etc. MODULO IS NOT SUPPORTED!
                equal_exists = False
                for i in range(len(operation_string)):
                    if is_floatable(
                            operation_string[i]) and equal_exists == False:
                        int_storage_var += operation_string[i]
                    elif operation_string[i] == ".":
                        int_storage_var += operation_string[i]
                    elif not is_floatable(operation_string[i]):
                        operation_list.append(int_storage_var)
                        operation_list.append(operation_string[i])
                        int_storage_var = ""
                    if i == len(operation_string) - 1:
                        operation_list.append(int_storage_var)
                    if operation_string[i] == "=":
                        equal_exists = True
                while "" in operation_list:
                    operation_list.remove("")
                return operation_list

            # Solves the string inputted. For example, 2*(3+5) would output 16.
            def solve_string(temp_expression):
                temp_expression = organize_expression(temp_expression)
                if len(temp_expression) <= 1:
                    temp_expression[0] = float(temp_expression[0])

                if ")" in temp_expression and not "(" in temp_expression:
                    print(
                        "A malfunction may have occured, as you have an open-ended parentheses. Or, you could have used [] or {} instead of ()."
                    )

                while "(" in temp_expression:
                    lower_range = temp_expression.index("(") + 1
                    try:
                        upper_range = temp_expression.index(")")
                    except IndexError:
                        # This here will be message.send in DISCORD!!!!!!
                        print(
                            "A malfunction may have occured, as you have an open-ended parentheses. Or, you could have used [] or {} instead of ()."
                        )
                        break
                    parentheses_expression_string = "".join(
                        temp_expression[lower_range:upper_range])
                    temp_expression[lower_range - 1] = solve_string(
                        parentheses_expression_string)[0]
                    while temp_expression[lower_range] != ")":
                        temp_expression.pop(lower_range)
                    temp_expression.pop(lower_range)

                while "^" in temp_expression:
                    indice = temp_expression.index("^")
                    temp_expression[indice - 1] = float(
                        temp_expression[indice - 1])**float(
                            temp_expression[indice + 1])
                    temp_expression.pop(indice)
                    temp_expression.pop(indice)

                while "*" in temp_expression or "/" in temp_expression:
                    if "*" in temp_expression and "/" in temp_expression:
                        indice = temp_expression.index("*")

                        indice2 = temp_expression.index("/")

                        if indice < indice2:
                            temp_expression[indice - 1] = float(
                                temp_expression[indice - 1]) * float(
                                    temp_expression[indice + 1])
                            temp_expression.pop(indice)
                            temp_expression.pop(indice)
                        elif indice2 < indice:
                            temp_expression[indice2 - 1] = float(
                                temp_expression[indice2 - 1]) / float(
                                    temp_expression[indice2 + 1])
                            temp_expression.pop(indice2)
                            temp_expression.pop(indice2)

                    elif "*" in temp_expression:
                        indice = temp_expression.index("*")
                        temp_expression[indice - 1] = float(
                            temp_expression[indice - 1]) * float(
                                temp_expression[indice + 1])
                        temp_expression.pop(indice)
                        temp_expression.pop(indice)
                    elif "/" in temp_expression:
                        indice2 = temp_expression.index("/")
                        temp_expression[indice2 - 1] = float(
                            temp_expression[indice2 - 1]) / float(
                                temp_expression[indice2 + 1])
                        temp_expression.pop(indice2)
                        temp_expression.pop(indice2)

                while "+" in temp_expression or "-" in temp_expression:
                    if "+" in temp_expression and "-" in temp_expression:
                        indice = temp_expression.index("+")
                        indice2 = temp_expression.index("-")
                        if indice < indice2:
                            temp_expression[indice - 1] = float(
                                temp_expression[indice - 1]) + float(
                                    temp_expression[indice + 1])
                            temp_expression.pop(indice)
                            temp_expression.pop(indice)
                        elif indice2 < indice:
                            temp_expression[indice - 1] = float(
                                temp_expression[indice - 1]) - float(
                                    temp_expression[indice + 1])
                            temp_expression.pop(indice2)
                            temp_expression.pop(indice2)

                    elif "+" in temp_expression:
                        indice = temp_expression.index("+")
                        temp_expression[indice - 1] = float(
                            temp_expression[indice - 1]) + float(
                                temp_expression[indice + 1])
                        temp_expression.pop(indice)
                        temp_expression.pop(indice)
                    elif "-" in temp_expression:
                        indice2 = temp_expression.index("-")
                        temp_expression[indice2 - 1] = float(
                            temp_expression[indice2 - 1]) - float(
                                temp_expression[indice2 + 1])
                        temp_expression.pop(indice2)
                        temp_expression.pop(indice2)
                try:
                    result = []
                except:
                    print("lol")
                for i in temp_expression:
                    if is_floatable(i):
                        result.append(i)
                return result

            # Transforms a word into a number.
            def word_to_number(string):
                word = string.lower()
                word_list = word.split(" ")
                units = [
                    "zero", "one", "two", "three", "four", "five", "six",
                    "seven", "eight", "nine", "ten", "eleven", "twelve",
                    "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
                    "eighteen", "nineteen"
                ]

                tens = [
                    "twenty", "thirty", "fourty", "fifty", "sixty", "seventy",
                    "eighty", "ninety"
                ]

                hundreds = [
                    "hundred", "thousand", "million", "billion", "trillion"
                ]

                for i in range(len(word_list)):
                    for j in range(20):
                        if units[j] == word_list[i]:
                            word_list[i] = j
                            break
                    for k in range(8):
                        if tens[k] == word_list[i]:
                            word_list[i] = 10 * (k + 2)
                            break
                    for l in range(5):
                        if hundreds[l] == word_list[i]:
                            if l == 0:

                                temp_list = word_list[:i]
                                while -1 in temp_list:
                                    temp_list.remove(-1)
                                while "and" in temp_list:
                                    temp_list.remove("and")
                                multiply_value = 0
                                for index, value in enumerate(temp_list):
                                    multiply_value += value
                                word_list[i] = multiply_value * 100
                                for x in range(i):
                                    word_list[x] = -1

                            else:
                                try:
                                    temp_list = word_list[:i]
                                    while -1 in temp_list:
                                        temp_list.remove(-1)
                                    while "and" in temp_list:
                                        temp_list.remove("and")
                                    multiply_value = 0
                                    for index, value in enumerate(temp_list):
                                        multiply_value += value
                                    word_list[i] = multiply_value * (1000**l)
                                    for x in range(i):
                                        word_list[x] = -1
                                except:
                                    word_list[i] = 1000**l

                while -1 in word_list:
                    word_list.remove(-1)
                while "and" in word_list:
                    word_list.remove("and")
                final_value = 0
                for index, value in enumerate(word_list):
                    final_value += value
                return final_value

            # Transforms roman numerals to numbers.
            def roman_to_number(text):
                roman_numeral_dict = {
                    "i": 1,
                    "v": 5,
                    "x": 10,
                    "l": 50,
                    "c": 100,
                    "d": 500,
                    "m": 1000
                }
                textlist = list(text.lower())
                print(textlist)
                final_value = 0
                temp_value = 0
                not_roman_numeral = False
                for i in range(len(textlist)):
                    if textlist[i] != "i" and textlist[i] != "v" and textlist[i] != "x" and textlist[i] != "l" and textlist[i] != "c" and textlist[i] != "d" and textlist[i] != "m":
                        not_roman_numeral = True
                        break
                    for key in roman_numeral_dict:
                        if textlist[len(textlist) - i - 1] == key:
                            if temp_value <= roman_numeral_dict[key]:
                                final_value += roman_numeral_dict[key]
                            else:
                                final_value -= roman_numeral_dict[key]
                            temp_value = roman_numeral_dict[key]
                if not_roman_numeral == True:
                  return 0
                else:
                  return final_value

            # Translates chinese numbers into english.

            def chinese_to_number(string):
                translator= Translator(from_lang ="chinese",to_lang="English")
                translation = translator.translate(str(string))
                try:
                    translation = roman_to_number(str(translation))
                except:
                    print("nope")
                print(int(translation))
                return int(translation)


                
            # The primary handler for deciding if a message response should increase the count or reset it.
            def increment(increment_value=1):
                global countlist
                global previous_person
                global response

                # These lists exist so that the computer is more sure that something is a word-number/roman numeral.
                num_list = [
                    "zero", "one", "two", "three", "four", "five", "six",
                    "seven", "eight", "nine", "ten", "eleven", "twelve",
                    "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
                    "eighteen", "nineteen", "twenty", "thirty", "fourty",
                    "fifty", "sixty", "seventy", "eighty", "ninety"
                ]
                roman_list = ['i', 'v', 'x', 'l', 'c', 'd', 'm']

                response = ""
                # Converts numerical words/equations into integral form, allowing the computer to proccess it further. This part will change the result variable according to what was inputted.

                if is_intable(message.content):
                    result = int(message.content)

                  
                # Credits: sedeh(from stackoverflow. Link here: https://stackoverflow.com/questions/38334937/python-check-if-a-key-in-a-dictionary-is-contained-in-a-string)
                elif any(x in message.content for x in num_list):
                    result = list(message.content)
                    while "-" in result:
                        hyphen_index = result.index("-")
                        result[hyphen_index] = " "
                    result = "".join(result)
                    print(result)
                    result = word_to_number(result)
                    print(result)

                elif "^" in message.content or "*" in message.content or "+" in message.content or "-" in message.content or "/" in message.content:
                    try:
                        result = solve_string(message.content)[0]
                    except:
                        result = 0
                # Same credits as the other statement above.
                elif any(z in message.content.lower() for z in roman_list):
                    # Beta implementation
                    if pumpcoin_dict[message.author.name] >= 30:
                      try:
                        result = roman_to_number(message.content)
                      except:
                        result = 0
                        print(result)

                else:
                    if pumpcoin_dict[message.author.name] >= 50:
                        try:
                            result = chinese_to_number(message.content)
                        except:
                            print("failed")
                    

                # This part checks the result, as well as checking whether you posted a number
                        

                if result == countlist[mychannel.guild.name][mychannel.name]:
                    if countlist[mychannel.guild.name][mychannel.name] == int(increment_value) or message.author.id != previous_person[mychannel.guild.name][mychannel.name]:
                        previous_person[mychannel.guild.name][
                            mychannel.name] = message.author.id
                        response = "count up"
                        countlist[mychannel.guild.name][mychannel.name] += int(
                            increment_value)
                        try:
                            pumpcoin_dict[message.author.name] += 1
                        except:
                            pumpcoin_dict[message.author.name] = 1
                    else:
                        response = "counted twice"
                        countlist[mychannel.guild.name][mychannel.name] = int(
                            increment_value)
                        previous_person[mychannel.guild.name][
                            mychannel.name] = -1  
                elif result != 0:        
                    response = "ruined the count"
                    countlist[mychannel.guild.name][mychannel.name] = int(
                        increment_value)
                    previous_person[mychannel.guild.name][mychannel.name] = -1
                if result == "Need More Pumpcoins":
                    response = "Need More Pumpcoins"
                return response

            if message.author.id != 990418726643986503:
                if message.channel.name == "pumpkin-counting" or message.channel.name == "counting" or message.channel.name == "gnitnuoc":
                    try:
                        output_of_function = increment(1)
                    except:
                        output_of_function = ""

                    if output_of_function == "ruined the count":
                        try:
                            await message.add_reaction(
                                "<:pumpkinperfection:990665501069946921>")
                        except:
                            await message.add_reaction("\N{CAT}")
                        await message.add_reaction('\N{THUMBS DOWN SIGN}')
                        await message.channel.send("Meow! Somebody ruined the count! Pumpkin is very mad, and has reset the count to 1.")

                    elif output_of_function == "counted twice":
                        try:
                            await message.add_reaction("<:pumpkinperfection:990665501069946921>")
                        except:
                            await message.add_reaction("\N{CAT}")
                        await message.add_reaction('\N{THUMBS DOWN SIGN}')
                        await message.channel.send(
                            "Meow! Somebody tried to count twice! Pumpkin is very mad, and has reset the count to 1."
                        )

                    elif output_of_function == "count up":
                        try:
                            await message.add_reaction("<:pumpkinperfection:990665501069946921>")
                        except:
                            await message.add_reaction("\N{CAT}")
                        await message.add_reaction('\N{THUMBS UP SIGN}')
                        try:
                            victorymessagevalue = messages[message.channel.guild.name]
                            await message.channel.send(victorymessagevalue)
                        except:
                            victorymessagevalue = ""
                            if globalvictorymessage != "":
                                await message.channel.send(globalvictorymessage)
                    elif output_of_function == "Need More Pumpcoins":
                        await message.channel.send("Meow! You need more pumpcoins to do that! You can get pumpcoins by just counting regularly.")

                elif "count" in message.channel.name or "Count" in message.channel.name:
                    channel_name = message.channel.name
                    if "-" in channel_name:
                        channel_name = channel_name.split("-")
                    else:
                        channel_name = channel_name.split()
                    index_of_by = channel_name.index("by")
                    count_by_value = channel_name[index_of_by + 1]
                    print(count_by_value)
                    try:
                        output_of_function = increment(count_by_value)
                    except:
                        output_of_function = ""
                    if output_of_function == "ruined the count":
                        try:
                            await message.add_reaction("<:pumpkinperfection:990665501069946921>")
                        except:
                            await message.add_reaction("\N{CAT}")
                        await message.add_reaction('\N{THUMBS DOWN SIGN}')
                        await message.channel.send("Meow! Somebody ruined the count! Pumpkin is very mad, and has reset the count to "+ str(count_by_value) +". REMEMBER, we are counting by " +str(count_by_value) +" here, and the FIRST NUMBER you type is " +str(count_by_value) + ".")
                    elif output_of_function == "counted twice":
                        try:
                          await message.add_reaction("<:pumpkinperfection:990665501069946921>")
                        except:
                          await message.add_reaction("\N{CAT}")
                        await message.add_reaction('\N{THUMBS DOWN SIGN}')
                        await message.channel.send("Meow! Somebody tried to count twice! Pumpkin is very mad, and has reset the count to  "+ str(count_by_value) + ".")

                    elif output_of_function == "count up":
                        try:
                            await message.add_reaction("<:pumpkinperfection:990665501069946921>")
                        except:
                            await message.add_reaction("\N{CAT}")
                        await message.add_reaction('\N{THUMBS UP SIGN}')
                        try:
                            victorymessagevalue = messages[message.channel.guild.name]
                            await message.channel.send(victorymessagevalue)
                        except:
                            victorymessagevalue = ""
                            if globalvictorymessage != "":
                                await message.channel.send(globalvictorymessage)
                            else:
                                print("lol")
        # This piece of code updates a discord message with all of the counting data.

        if debug_mode == "off":
            Temp_storage = {}
            Temp_storage["countlist"] = countlist
            Temp_storage["previous_person"] = previous_person
            Temp_storage["messages"] = messages
            Temp_storage["globalvictorymessage"] = globalvictorymessage
            countdata_channel = client.get_channel(1008040131879522356)
            pumpcoin_channel = client.get_channel(1008040158597234758) 
            counting_message = await countdata_channel.fetch_message(1008041694261936218)
            pumpcoin_message = await pumpcoin_channel.fetch_message(1008041694706548737)
            await counting_message.edit(content=str(Temp_storage))
            await pumpcoin_message.edit(content=str(pumpcoin_dict))

            time.sleep(0.3)



# DO NOT DELETE! Credits: Mathemolympiad
running()
secret = os.environ['token']
try:
  client.run(secret)
except:
  requests.get('https://PingMachine.danielchen1464.repl.co/botIsDown?name=pumpkin')