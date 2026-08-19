from  audio007.carrinho import Carrinho

    
with Carrinho(modo='eleva') as c: 
    c.raio = 650         #original=800
    c.espera(c.zera())  #pro raio velho de 800 mm
    c.espera(c.anda_mm('grande', +150)) # pro raio novo de 650 mm
    c.espera(c.anda_azim_mirado(0))
    c.espera(c.anda_mm('grande', -150)) # pro raio novo de 650 mm ---- ta rodando ao inves de descer
    c.espera(c.anda_azim_mirado(-90))

    input('qqer tecla para terminar')
