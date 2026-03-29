from flask import Flask, request, jsonify
import json

app = Flask(__name__)

ARQUIVO = 'dados.json'

# Função para ler dados
def ler_dados():
    try:
        with open(ARQUIVO, 'r') as f:
            return json.load(f)
    except:
        return []

# Função para salvar dados
def salvar_dados(dados):
    with open(ARQUIVO, 'w') as f:
        json.dump(dados, f, indent=4)

# 🔹 CREATE
@app.route('/produtos', methods=['POST'])
def criar_produto():
    dados = ler_dados()
    novo = request.json

    novo['id'] = len(dados) + 1
    dados.append(novo)

    salvar_dados(dados)
    return jsonify(novo), 201

# 🔹 READ
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    return jsonify(ler_dados())

# 🔹 UPDATE
@app.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    dados = ler_dados()

    for produto in dados:
        if produto['id'] == id:
            produto.update(request.json)
            salvar_dados(dados)
            return jsonify(produto)

    return jsonify({'erro': 'Produto não encontrado'}), 404

# 🔹 DELETE
@app.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    dados = ler_dados()

    for produto in dados:
        if produto['id'] == id:
            dados.remove(produto)
            salvar_dados(dados)
            return jsonify({'mensagem': 'Produto removido'})

    return jsonify({'erro': 'Produto não encontrado'}), 404

# Rodar servidor
if __name__ == '__main__':
    app.run(debug=True)