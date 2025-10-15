from config import app, db
from models import Aluno, Curso, Matricula
from flask import request, jsonify, render_template, redirect, url_for


@app.route('/')
def index():
    return render_template('index.html')


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


@app.route('/cursos')
def listar_cursos():
    cursos = Curso.query.all()
    return render_template('cursos.html', cursos=cursos)


@app.route('/novo_curso', methods=['GET', 'POST'])
def novo_curso():
    if request.method == 'POST':
        nome = request.form['nome']
        curso = Curso(nome=nome)
        db.session.add(curso)
        db.session.commit()
        return redirect(url_for('listar_cursos'))
    return render_template('novo_curso.html')


@app.route('/nova_matricula', methods=['GET', 'POST'])
def nova_matricula():
    alunos = Aluno.query.all()
    cursos = Curso.query.all()
    if request.method == 'POST':
        aluno_id = request.form['aluno_id']
        curso_id = request.form['curso_id']
        matricula = Matricula(aluno_id=aluno_id, curso_id=curso_id)
        db.session.add(matricula)
        db.session.commit()
        return redirect(url_for('relatorio'))
    return render_template('nova_matricula.html', alunos=alunos, cursos=cursos)


@app.route('/alunos', methods=['GET'])
def render_alunos():
    alunos = Aluno.query.all()
    return render_template('alunos.html', alunos=alunos)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
