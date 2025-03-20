from time import strftime

from flask import Flask, jsonify
from flask_pydantic_spec import FlaskPydanticSpec

from datetime import date

tempo = date.today()

print(f'ano {tempo.year}')
print(f'mes {tempo.month}')
print(f'dia {tempo.day}')

app = Flask(__name__)
spec = FlaskPydanticSpec('flask',
                         title='Flask API',
                         version='1.0')
spec.register(app)


@app.route("/")
def hello_world():
    return f'ola Mundo!'


@app.route("/<ano>/<mes>/<dia>")
def data(ano, mes, dia):
    """
        API para calcular a diferenças entre as duas datas
        ### Endpoint:
            GET /<ano>/<mes>/<dia>

        ### Parameters:
        - ano (str)
        - mes (str)
        - dia (str)


        ### Returns:
        ```json
            {
                "situacao": passado,
                "dias de diferenca": 365,
                "meses de diferenca": 12,
                "anos de diferenca": 1
            }
        ```
        ## Erros possiveis:
         - se a `data` inserida não for no formato date corretamente retorna mensagem de ** erro 400 Bad Request **
    """
    try:
        tempo_recebido = date(int(ano), int(mes), int(dia))

        if tempo.year < tempo_recebido.year:
            situacao = 'futuro'
        elif tempo.year > tempo_recebido.year:
            situacao = 'passado'
        else:
            situacao = 'presente'
        delta = tempo_recebido - tempo
        dias_diferenca = delta.days
        meses_diferenca = abs(tempo.year - tempo_recebido.year) * 12 + abs(tempo.month - tempo_recebido.month)
        anos_diferenca = tempo.year - tempo_recebido.year
        return jsonify({'situacao': situacao,
                        'dias de diferenca': abs(dias_diferenca),
                        'meses_diferenca': abs(meses_diferenca),
                        'ano de diferenca': abs(anos_diferenca)
                        })
    except ValueError:
        return f'data inserida invalida'
    except TypeError:
        return jsonify({'erro 400': 'formato de data invalido',},400)



if __name__ == "__main__":
    app.run(debug=True)
