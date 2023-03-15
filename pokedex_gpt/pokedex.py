import openai,config,json
from rich import print
from rich.table import Table


def main():

    openai.api_key = config.api_key

    print("[bold green]Pokedex GPT in Python[/bold green]")

    options = Table("comando", "Descripción")
    options.add_row("exit", "Salir de la aplicación")

    print(options)

    message = [{"role":"system",
                "content":"eres un pokedex, que genera una diccionrio conla siguiente informacion ID, Nombre, Altura en int, Peso en int, Tipo, Habilidades, Estadísticas, Velocidad del pokemon que va en el endpoint"},
                {"role":"system",
                 "content":"si no hay información, reponde que 'Ingresa un pokemon valido'"}]

    while True:

        content = input("¿Que pokemon quieres ver?\n")

        if content == "exit":
            break

        message.append({"role":"user","content":f"https://pokeapi.co/api/v2/pokemon/{content}"})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",messages=message)
        
        response = response.choices[0].message.content
        pokedex(response)
        
        message.append({"role":"assistant","content":response})


def pokedex(response):

    # clean response
    response = response.replace("```","").replace("\n","")
    response = response[response.index("{")::]
    response = json.loads(response)

    pokedex = Table(response["Nombre"].upper(), "Caracteristicas")
    pokedex.add_row("id", str(response["ID"]))
    pokedex.add_row("Altura", str(response["Altura"]/10)+'m')
    pokedex.add_row("Peso", str(response["Peso"]/10)+'Kg')
    pokedex.add_row("Tipo", str(response["Tipo"]))
    pokedex.add_row("Habilidades", str(response["Habilidades"]))
    pokedex.add_row("Estadísticas", str(response["Estadísticas"]))
    pokedex.add_row("Velocidad", str(response["Velocidad"]/10)+"m/s")

    print(pokedex)

if __name__ == '__main__':
    main()
