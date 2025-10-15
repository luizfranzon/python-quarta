from config import app, db
from models import Aluno, Curso, Matricula
from flask import request, jsonify


@app.route('/api/alunos', methods=['POST'])
def criar_aluno_api():
    dados = request.json
    aluno = Aluno(nome=dados['nome'], idade=dados['idade'])
    db.session.add(aluno)
    db.session.commit()
    return jsonify({'id': aluno.id})


@app.route('/api/alunos', methods=['GET'])
def listar_alunos_api():
    alunos = Aluno.query.all()
    return jsonify([{'id': a.id, 'nome': a.nome, 'idade': a.idade} for a in alunos])


@app.route('/api/matriculas', methods=['POST'])
def criar_matricula_api():
    dados = request.json
    matricula = Matricula(aluno_id=dados['aluno_id'], curso_id=dados['curso_id'])
    db.session.add(matricula)
    db.session.commit()
    return jsonify({'id': matricula.id})


@app.route('/api/relatorio', methods=['GET'])
def relatorio_api():
    resultado = db.session.query(Aluno.nome, Curso.nome).join(Matricula).join(Curso).all()
    return jsonify([{'aluno': r[0], 'curso': r[1]} for r in resultado])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
