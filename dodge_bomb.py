import sys
import pygame as pg
import random

WIDTH, HEIGHT = 1600, 900

delta = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}

def check_bound(rect: pg.Rect) -> tuple[bool, bool]:
    """
    こうかとんRect，爆弾Rectが画面外 or 画面内かを判定する関数
    引数：こうかとんRect or 爆弾Rect
    戻り値：横方向，縦方向の判定結果タプル（True：画面内／False：画面外）
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:  # 横方向判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


def kk_k():
    kk_img0 = pg.transform.rotozoom(pg.image.load("ex02/fig/3.png"), 0, 2.0)
    kk_img1 = pg.transform.flip(kk_img0, True, False)
    return{(0, 0):kk_img0, 
           (-5, 0):kk_img0,
           (-5, -5):pg.transform.rotozoom(kk_img0, -45, 1.0),
           (-5, +5):pg.transform.rotozoom(kk_img0, 45, 1.0),
           (0, -5):pg.transform.rotozoom(kk_img1, 90, 1.0),
           (+5, -5):pg.transform.rotozoom(kk_img1, 45, 1.0),
           (+5, 0):pg.transform.rotozoom(kk_img1, 0, 1.0),
           (+5, +5):pg.transform.rotozoom(kk_img1, -45, 1.0),
           (0, +5):pg.transform.rotozoom(kk_img1, -90, 1.0)}  #演習1



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)

    kk_imgs = kk_k()
    kk_img = kk_imgs[(0,0)]

    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bd_img = pg.Surface((20, 20))
    bd_img.set_colorkey((0,0,0))
    pg.draw.circle(bd_img, (255, 0, 0), (10, 10), 10)
    x = random.randint(0,WIDTH)
    y = random.randint(0,HEIGHT)
    bd_rct = bd_img.get_rect()
    bd_rct.center = x,y
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0


    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bd_rct):  # 練習５
            print("ゲームオーバー")
            return   # ゲームオーバー
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]  # 合計移動量
        for k, mv in delta.items():
            if key_lst[k]: 
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        kk_img = kk_imgs[tuple(sum_mv)]
        screen.blit(bg_img, [0, 0])
        screen.blit(kk_img, kk_rct)
        bd_rct.move_ip(vx, vy)

        yoko, tate = check_bound(bd_rct)
        if not yoko:  # 横方向に画面外だったら
            vx *= -1
        if not tate:  # 縦方向に範囲外だったら
            vy *= -1

        screen.blit(bd_img,bd_rct)
        pg.display.update()
        tmr += 1
        clock.tick(10)
        #clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()