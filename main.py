import pygame
import random

# Configurações Globais
LARGURA, ALTURA = 400, 600
FPS = 60

class JogoCarro:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Car Dodge: Antigravity Edition")
        self.relogio = pygame.time.Clock()
        
        try:
            surface_jogador = pygame.image.load("player_car.png").convert()
            surface_jogador.set_colorkey(surface_jogador.get_at((0, 0)))
            self.img_jogador = pygame.transform.scale(surface_jogador, (50, 80))

            surface_inimigo = pygame.image.load("enemy_car.png").convert()
            surface_inimigo.set_colorkey(surface_inimigo.get_at((0, 0)))
            self.img_inimigo = pygame.transform.scale(surface_inimigo, (50, 80))
        except Exception:
            self.img_jogador = None
            self.img_inimigo = None

        self.reset_jogo()

    def reset_jogo(self):
        self.jogador = pygame.Rect(LARGURA//2 - 25, ALTURA - 100, 50, 80)
        self.inimigos = []
        self.spawn_timer = 0
        self.pontos = 0
        self.game_over = False
        self.esta_pulando = False
        self.tempo_pulo = 0

    def mostrar_texto(self, texto, tamanho, y):
        fonte = pygame.font.SysFont("Arial", tamanho, True)
        render = fonte.render(texto, True, (255, 255, 255))
        rect = render.get_rect(center=(LARGURA//2, y))
        self.tela.blit(render, rect)

    def rodar(self):
        while True:
            self.tela.fill((50, 50, 50)) # Estrada
            
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: return
                if ev.type == pygame.KEYDOWN:
                    if self.game_over and ev.key == pygame.K_RETURN:
                        self.reset_jogo()
                    if not self.game_over and ev.key == pygame.K_SPACE and not self.esta_pulando:
                        self.esta_pulando = True
                        self.tempo_pulo = 20 # Duração do vôo

            if not self.game_over:
                self.atualizar()
                self.desenhar()
            else:
                self.mostrar_texto("BATEU!", 50, ALTURA//2 - 50)
                self.mostrar_texto(f"Pontos: {self.pontos}", 30, ALTURA//2 + 10)
                self.mostrar_texto("ENTER para reiniciar", 20, ALTURA//2 + 60)

            pygame.display.flip()
            self.relogio.tick(FPS)

    def atualizar(self):
        teclas = pygame.key.get_pressed()
        vel = 6
        if teclas[pygame.K_LEFT] and self.jogador.left > 0: self.jogador.x -= vel
        if teclas[pygame.K_RIGHT] and self.jogador.right < LARGURA: self.jogador.x += vel
        if teclas[pygame.K_UP] and self.jogador.top > 0: self.jogador.y -= vel
        if teclas[pygame.K_DOWN] and self.jogador.bottom < ALTURA: self.jogador.y += vel

        # Lógica de Antigravidade (Pulo)
        if self.esta_pulando:
            self.tempo_pulo -= 1
            if self.tempo_pulo <= 0: self.esta_pulando = False

        # Spawn de inimigos: ficam mais rápidos e aparecem mais frequentemente
        self.spawn_timer += 1
        limite_spawn = max(15, 40 - (self.pontos // 2))
        if self.spawn_timer > limite_spawn:
            self.inimigos.append(pygame.Rect(random.randint(0, LARGURA-50), -100, 50, 80))
            self.spawn_timer = 0

        # Mover inimigos e colisão
        for inimigo in self.inimigos[:]:
            inimigo.y += 7 + (self.pontos // 3) # Aumenta a velocidade drasticamente
            if inimigo.top > ALTURA:
                self.inimigos.remove(inimigo)
                self.pontos += 1
            
            # Só morre se NÃO estiver pulando (Antigravidade!)
            if self.jogador.colliderect(inimigo) and not self.esta_pulando:
                self.game_over = True

    def desenhar(self):
        # Desenha Jogador
        if self.img_jogador:
            if self.esta_pulando:
                self.img_jogador.set_alpha(150) # Fica semi-transparente quando pula
            else:
                self.img_jogador.set_alpha(255)
            self.tela.blit(self.img_jogador, self.jogador.topleft)
        else:
            cor_player = (0, 255, 255) if self.esta_pulando else (0, 100, 255)
            pygame.draw.rect(self.tela, cor_player, self.jogador)
        
        # Desenha Inimigos
        for inimigo in self.inimigos:
            if self.img_inimigo:
                self.tela.blit(self.img_inimigo, inimigo.topleft)
            else:
                pygame.draw.rect(self.tela, (255, 50, 50), inimigo)
        
        self.mostrar_texto(f"Pontos: {self.pontos}", 25, 30)
        if self.esta_pulando:
            self.mostrar_texto("MODO ANTIGRAVIDADE ATIVO!", 15, 60)

if __name__ == "__main__":
    JogoCarro().rodar()
