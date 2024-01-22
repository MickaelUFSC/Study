from django.shortcuts import render, redirect
from .models import Categoria, Flashcard, Desafio, FlashcardDesafio
from django.contrib import messages
from django.http import HttpResponse

def novo_flashcard(request):
    if request.user.is_authenticated == False:
        return redirect('/usuarios/logar')
    
    if request.method == "GET":
        categoria = Categoria.objects.all()
        dificuldade = Flashcard.DIFICULDADE_CHOICES
        fleshcards = Flashcard.objects.filter(user=request.user)
        categoria_filtrar = request.GET.get('categoria')
        dificuldade_filtrar = request.GET.get('dificuldade')
        if categoria_filtrar:
            fleshcards = fleshcards.filter(categoria=categoria_filtrar)
        if dificuldade_filtrar:
            fleshcards = fleshcards.filter(dificuldade=dificuldade_filtrar)
        
        return render(request, 'novo_flashcard.html', 
                      {'categorias': categoria, 
                       'dificuldades': dificuldade,
                       'flashcards': fleshcards})

    elif request.method == "POST":
        pergunta = request.POST.get('pergunta')
        resposta = request.POST.get('resposta')
        categoria = request.POST.get('categoria')
        dificuldade = request.POST.get('dificuldade')
        
        if len(pergunta.strip()) == 0 or len(resposta.strip()) == 0:
            messages.add_message(request, messages.ERROR, 
                                 'Preencha todos os campos!')
            return redirect('/flashcard/novo_flashcard')
        
        flashcard = Flashcard(user=request.user, 
                              pergunta=pergunta, 
                              resposta=resposta, 
                              categoria_id=categoria, 
                              dificuldade=dificuldade)
        flashcard.save()
        messages.add_message(request, messages.SUCCESS, 
                             'Flashcard cadastrado com sucesso!')
        return redirect('/flashcard/novo_flashcard')
    
def deletar_flashcard(request, id):
    if request.user.is_authenticated == False:
        return redirect('/usuarios/logar')
    
    flashcard = Flashcard.objects.get(id=id)
    if flashcard.user != request.user:
        messages.add_message(request, messages.ERROR, 
                             'Você não pode deletar esse flashcard!')
        return redirect('/flashcard/novo_flashcard')
    else:
        flashcard.delete()
        messages.add_message(request, messages.SUCCESS, 
                         'Flashcard deletado com sucesso!')
        return redirect('/flashcard/novo_flashcard')
    
def iniciar_desafio(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        return render(
            request,
            'iniciar_desafio.html',
            {'categorias': categorias, 'dificuldades': dificuldades},
        )
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        categorias = request.POST.getlist('categoria')
        dificuldade = request.POST.get('dificuldade')
        qtd_perguntas = request.POST.get('qtd_perguntas')
        desafio = Desafio(
            user=request.user,
            titulo=titulo,
            quantidade_perguntas=qtd_perguntas,
            dificuldade=dificuldade,
        )
        desafio.save()
        desafio.categoria.add(*categorias)
        flashcards = (
            Flashcard.objects.filter(user=request.user)
            .filter(dificuldade=dificuldade)
            .filter(categoria_id__in=categorias)#filtra as categorias selecionadas pelo usuario e que estejam na lista de categorias do flashcard 
            .order_by('?') #tras os flashcards de forma aleatoria
        )
        if flashcards.count() < int(qtd_perguntas):
            return redirect('/flashcard/iniciar_desafio/')
        flashcards = flashcards[: int(qtd_perguntas)]
        for f in flashcards:
            flashcard_desafio = FlashcardDesafio(
                flashcard=f,
            )
            flashcard_desafio.save()
            desafio.flashcards.add(flashcard_desafio)
        desafio.save()
        return redirect(f'/flashcard/desafio/{desafio.id}')


def listar_desafio(request):
    desafios = Desafio.objects.filter(user=request.user)
    return render(request,'listar_desafio.html',
        {'desafios': desafios})
    
def desafio(request, id):
    desafio = Desafio.objects.get(id=id)
    if not desafio.user == request.user:
        raise Http404()

    if request.method == 'GET':
        acertos = desafio.flashcards.filter(respondido=True).filter(acertou=True).count()
        erros = desafio.flashcards.filter(respondido=True).filter(acertou=False).count()
        faltantes = desafio.flashcards.filter(respondido=False).count()
        return render(request,'desafio.html',{'desafio': desafio,'acertos': acertos, 'erros': erros, 'faltantes': faltantes})

def responder_flashcard(request, id):
    flashcard_desafio = FlashcardDesafio.objects.get(id=id)
    acertou = request.GET.get('acertou')
    desafio_id = request.GET.get('desafio_id')
    flashcard_desafio.respondido = True
    flashcard_desafio.acertou = True if acertou == '1' else False
    flashcard_desafio.save()
    return redirect(f'/flashcard/desafio/{desafio_id}/')

def relatorio(request, id):
    desafio = Desafio.objects.get(id=id)
    acertos = desafio.flashcards.filter(acertou=True).count()
    erros = desafio.flashcards.filter(acertou=False).count()
    
    dados = [acertos, erros]
    
    categorias = desafio.categoria.all()
    name_categoria = [i.nome for i in categorias]
    dados2 = []
    for categoria in categorias:
        dados2.append(desafio.flashcards.filter(flashcard__categoria=categoria).filter(acertou=True).count()) #acessa a foreing key flashcard e filtra pela categoria
    return render(request, 'relatorio.html', {'desafio': desafio, 'dados':dados, 
                                              'categorias':name_categoria, 'dados2':dados2},)

 