# TEE PELI TÄHÄN
import pygame
import random

class Keraily:
    def __init__(self):
        pygame.init()
        self.siirrot = 0
        self.peliohi = False
        self.lataa_kuvat()
        self.uusi_kartta()
        
        self.kolikot = 0
        
        self.korkeus = len(self.kartta)
        self.leveys = len(self.kartta[0])
        self.skaala = self.kuvat[0].get_width()

        nayton_korkeus = self.skaala * self.korkeus
        nayton_leveys = self.skaala * self.leveys
        self.naytto = pygame.display.set_mode((nayton_leveys, nayton_korkeus + self.skaala))
        self.fontti = pygame.font.SysFont("Arial", 24)

        pygame.display.set_caption("Rahan etsintä")

        self.silmukka()

    def lataa_kuvat(self):
        self.kuvat = []
        for nimi in ["lattia", "seina", "kolikko", "hirvio", "robo", "kohderobo"]:
            self.kuvat.append(pygame.image.load(nimi + ".png"))

    def uusi_kartta(self):
        self.kartta = [[] for _ in range(20)]
        for i in range(20):
            for _ in range(20):
                if i % 2 == 0:
                    self.kartta[i].append(random.randrange(0, 4))
                else:
                    self.kartta[i].append(random.randrange(0,3))
        while True:
            x, y = random.randrange(0,20), random.randrange(0,20)
            if self.kartta[y][x] == 0:
                self.kartta[y][x] = 4
                break

        

    def silmukka(self):
        while True:
            self.tutki_tapahtumat()
            self.piirra_naytto()

    def tutki_tapahtumat(self):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_LEFT:
                    self.liiku(0, -1)
                if tapahtuma.key == pygame.K_RIGHT:
                    self.liiku(0, 1)
                if tapahtuma.key == pygame.K_UP:
                    self.liiku(-1, 0)
                if tapahtuma.key == pygame.K_DOWN:
                    self.liiku(1, 0)


                if tapahtuma.key == pygame.K_s:
                    self.uusi_kartta()
                    
                if tapahtuma.key == pygame.K_ESCAPE:
                    quit()

            if tapahtuma.type == pygame.QUIT:
                exit()
        

    def liiku(self, liike_y, liike_x):
        if self.peli_lapi():
            return
        robon_vanha_y, robon_vanha_x = self.etsi_robo()
        robon_uusi_y = robon_vanha_y + liike_y
        robon_uusi_x = robon_vanha_x + liike_x

        if self.kartta[robon_uusi_y][robon_uusi_x] == 1:
            return

        if self.kartta[robon_uusi_y][robon_uusi_x] == 3: # mörkkö
            self.peliohi = True
            return

        if self.kartta[robon_uusi_y][robon_uusi_x] == 2:# kolikko
            self.kolikot += 1
            self.kartta[robon_vanha_y][robon_vanha_x] -= 4 # robotti lattiaksi
            self.kartta[robon_uusi_y][robon_uusi_x] += 2 # kolikko robotiksi

        else:
            self.kartta[robon_vanha_y][robon_vanha_x] -= 4
            self.kartta[robon_uusi_y][robon_uusi_x] += 4
        
        self.siirrot += 1

    def etsi_robo(self):
        for y in range(self.korkeus):
            for x in range(self.leveys):
                if self.kartta[y][x] in [4, 6]:
                    return (y, x)


    def peli_lapi(self):
        if self.kolikot < 40:
            return False
        return True

    def piirra_naytto(self):
        self.naytto.fill((0, 0, 0))

        for y in range(self.korkeus):
            for x in range(self.leveys):
                ruutu = self.kartta[y][x]
                self.naytto.blit(self.kuvat[ruutu], (x * self.skaala, y * self.skaala))

        if self.peli_lapi():
            teksti = self.fontti.render(f"Onnittelut, läpäisit pelin! Ehdit kerätä yli {self.kolikot} kolikkoa", True, (255, 0, 0))
            teksti_x = self.skaala * self.leveys / 2 - teksti.get_width() / 2
            teksti_y = self.skaala * self.korkeus / 2 - teksti.get_height() / 2
            pygame.draw.rect(self.naytto, (0, 0, 0), (teksti_x, teksti_y, teksti.get_width(), teksti.get_height()))
            self.naytto.blit(teksti, (teksti_x, teksti_y))
            
            

        if self.peliohi:
            self.naytto.fill((0,0,0))
            teksti = self.fontti.render(f"Peli on ohi. Törmäsit mörkköön. Ehdit kerätä {self.kolikot} kolikkoa", True, (255, 0, 0))
            teksti_x = self.skaala * self.leveys / 2 - teksti.get_width() / 2
            teksti_y = self.skaala * self.korkeus / 2 - teksti.get_height() / 2
            pygame.draw.rect(self.naytto, (0, 0, 0), (teksti_x, teksti_y, teksti.get_width(), teksti.get_height()))
            self.naytto.blit(teksti, (teksti_x, teksti_y))
            
        
        teksti = self.fontti.render("Kolikot: " + str(self.kolikot), True, (255, 0, 0))
        self.naytto.blit(teksti, (25, self.korkeus * self.skaala + 10))

        teksti = self.fontti.render("S = uusi peli", True, (255, 0, 0))
        self.naytto.blit(teksti, (200, self.korkeus * self.skaala + 10))

        teksti = self.fontti.render("Esc = sulje peli", True, (255, 0, 0))
        self.naytto.blit(teksti, (400, self.korkeus * self.skaala + 10))

        teksti = self.fontti.render("KERÄÄ YLI 40 KOLIKKOA", True, (255, 0, 0))
        self.naytto.blit(teksti, (600, self.korkeus * self.skaala + 10))

        pygame.display.flip()

if __name__ == "__main__":
    Keraily()