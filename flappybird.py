import pygame, sys
import os
import random

#파이게임 초기화
pygame.init()

#창 제목 설정
pygame.display.set_caption("Pingu's Adventure")

#파이게임 화면 크기 설정
screen = pygame.display.set_mode((1280, 720))

#변수들 초기화
cpath = os.path.dirname(__file__)
gy = 0
x, y, w, h = 100, 720 / 2, 50, 50
pipex, pipey, pipew, pipeh = [1280,  1280 + 1280 // 3, 1280 + 1280 * 2 // 3],\
     [random.randint(720/2, 720/2 + 100),random.randint(720/2, 720/2 + 100),random.randint(720/2, 720/2 + 100)], 50, 500
move_dir = [0, 0, 0]
pipe_img_w, pipe_img_h = 100, 550
score = 0
font1 = pygame.font.SysFont(None,30)
game_over = False
first_game_over = True
first_changed = False
player_img = pygame.image.load(os.path.join(cpath, "resources/pingu2.png"))
game_over_img = pygame.image.load(os.path.join(cpath, "resources/gameover.png"))
pipe_img = pygame.image.load(os.path.join(cpath, "resources/pipe.png"))
pipe1_img = pygame.image.load(os.path.join(cpath, "resources/pipe1.png"))
tree_img = pygame.image.load(os.path.join(cpath, "resources/tree.png"))
tree1_img = pygame.image.load(os.path.join(cpath, "resources/tree1.png"))
title_img = [pygame.image.load(os.path.join(cpath, "resources/title.png")), \
             pygame.image.load(os.path.join(cpath, "resources/title2.png")), \
             pygame.image.load(os.path.join(cpath, "resources/title3.png"))]
setting_img = pygame.image.load(os.path.join(cpath, "resources/setting.png"))
back_img = pygame.image.load(os.path.join(cpath, "resources/back.png"))
face_img = pygame.image.load(os.path.join(cpath, "resources/PinguFace.png"))
mouth_img = pygame.image.load(os.path.join(cpath, "resources/PinguMouth.png"))
gamestart_img=[pygame.image.load(os.path.join(cpath, "resources/gamestart.png")), \
               pygame.image.load(os.path.join(cpath, "resources/gamestart1.png")), \
               pygame.image.load(os.path.join(cpath, "resources/gamestart2.png"))]
background_img = [pygame.image.load(os.path.join(cpath, "resources/background.png")).convert(), \
                  pygame.image.load(os.path.join(cpath, "resources/nam.png")).convert(), \
                  pygame.image.load(os.path.join(cpath, "resources/background_pixel.png")).convert()]
mawang_background_img = [pygame.image.load(os.path.join(cpath, "resources/background_mawang.png")).convert(), \
                         pygame.image.load(os.path.join(cpath, "resources/ma.png")).convert(), \
                         pygame.image.load(os.path.join(cpath, "resources/background_pixel_mawang.png")).convert()]
background_setting = 0
high_score = 0
pipe_base_speed = 5
pipe_increase_speed = -15
pipe_stop = False
first_changed2 = True
lr_rev_mode = False
pipe_stop_mode = False
pipe_move_mode = False
boss_mode = False
change_score = 5
stop_score = 10
move_mode_score = 15
boss_mode_score = 20
boss_x, boss_y = -400, 720 / 2 - 300 / 2
mouth_x = 0
fire = 0
ty = 720 / 2 - 300 / 2

jump_count = 3

main_scene = True
is_setting_mode = False
mySound = pygame.mixer.Sound(os.path.join(cpath, "resources/juuuuuump.wav"))
mySound2 = pygame.mixer.Sound("resources/121Nootnoot2.wav")
 
#게임 다시시작할 때 변수들 초기화
def game_restart():
    global gy, x, y, w, h, pipex, pipey, pipew, pipeh, score, game_over, first_game_over,\
        first_changed, pipe_stop, first_changed2, lr_rev_mode, jump_count, pipe_stop_mode, pipe_move_mode,\
        boss_mode, boss_x, boss_y, mouth_x, fire, ty
    gy = 0
    x, y, w, h = 100, 720 / 2, 50, 50
    #파이프 x, y, 너비, 높이
    pipex, pipey, pipew, pipeh = [1280,  1280 + 1280 // 3, 1280 + 1280 * 2 // 3],\
        [random.randint(720/2, 720/2 + 100),random.randint(720/2, 720/2 + 100),random.randint(720/2, 720/2 + 100)], 50, 500
    score = 0
    game_over = False
    first_changed = False
    first_changed2 = True
    first_game_over = True
    pipe_stop = False
    lr_rev_mode = False
    pipe_stop_mode = False
    pipe_move_mode = False
    boss_mode = False
    jump_count = 3
    boss_x, boss_y = -400, 720 / 2 - 300 / 2
    mouth_x = 0
    fire = 0
    ty = 720 / 2 - 300 / 2
    mySound2.stop()


#좌표, 가로 크기, 세로 크기가 주어졌을 때 충돌 했는지 체크
def collide(x, y, w, h, x_, y_, w_, h_):
    return x < x_ + w_ and y < y_ + h_ and x + w > x_ and y + h > y_

def dist(x1, x2):
    return abs(x1 - x2)

def pl_nearest_pipe():
    li = [dist(pipex[0], x), dist(pipex[1], x), dist(pipex[2], x)]
    if min(li) == dist(pipex[0], x):
        return 0
    elif min(li) == dist(pipex[1], x):
        return 1
    return 2

#그 뭐시기 그 그 그 FPS 그거 할려고 설정 할려고
clock = pygame.time.Clock()

bgm = pygame.mixer.Sound('resources/stage_bgm.wav')
mawang_bgm = pygame.mixer.Sound("resources/mawang.wav")
bgm.set_volume(1.0)

while 1:
    #FPS를 60으로 설정
    clock.tick(60)
    #파이게임 기본 코드 
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        #키가 눌렸다면
        if event.type==pygame.KEYDOWN:
            #눌린 키가 스페이스라면 점프
            if event.key == pygame.K_SPACE:
                if main_scene and not is_setting_mode:
                    game_restart()
                    bgm.play()
                    main_scene=False
                else:
                    if not game_over and not is_setting_mode:
                        gy = 10.5
                        mySound.play()
                        if pipe_stop_mode:
                            jump_count -= 1
                            if jump_count == 0:
                                pipe_stop_mode = False
                                pipe_stop = False
                                score += 1
                    else:
                        game_restart()
                        main_scene = True
  
        if event.type==pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            x_ = mouse_pos[0]
            y_ = mouse_pos[1]
            if is_setting_mode: 
                if x_ >= 10 and x_ <= 110 and y_ >= 10 and y_ <= 110:
                    is_setting_mode = False
                else:
                    background_setting += 1
                    background_setting %= 3

            elif main_scene:
                #설정 버튼 클릭했을때
                if x_ >= 1100 and x_ <= 1200 and y_ >= 600 and y_ <= 700:
                    is_setting_mode = True
                elif x_ >= 640-150 and x_ <= 640+150 and y_ >= 400 and y_ <= 500:
                    main_scene = False
                    bgm.play()
            else:
                if not game_over:
                    gy = 10.5
                    mySound.play()
                    if pipe_stop_mode:
                        jump_count -= 1
                        if jump_count == 0:
                            pipe_stop_mode = False
                            pipe_stop = False
                            score += 1


    if not main_scene:
        #배경색을 흰색으로 채우기
        back_color = (255,255,255)
        if score >= change_score:
            screen.blit(mawang_background_img[background_setting], (0,0))
            back_color = (0,0,0)
        else:
            screen.blit(background_img[background_setting], (0, 0))
        
        if score >= change_score:
            if not first_changed:
                first_changed = True
                bgm.stop()
                mawang_bgm.play()

        if score >= change_score - 2  and score < change_score and x < 1180 and not game_over:
            pipe_stop = True
            x += pipe_base_speed
            if x >= 1180 and first_changed2:
                score += 2
                first_changed2 = False
                lr_rev_mode = True
        else:
            pipe_stop = False

        if score == stop_score and abs(pipex[pl_nearest_pipe()] - x) <= 10:
            pipe_stop = True
            pipe_stop_mode = True

        if score == move_mode_score:
            pipe_move_mode = True

        if score == boss_mode_score:
            boss_mode = True
        
        if not game_over:
            #중력 설정
            gy -= 0.5
            #y값을 중력값에 따라 떨어지게
            y -= gy

        #플레이어 화면에 그리기
        player_color = (0, 0, 255) 
        if score >= change_score:
            player_color = (255, 0, 0)


        '''
        pygame.draw.rect(screen, (0, 255, 0), [x - w / 2, y - h / 2, w, h])
        pygame.draw.rect(screen, back_color, [x - w / 2 + 5, y - h / 2 + 5, w - 10, h - 10])
        '''

        screen.blit(player_img, (x - 25, y - 25))
        
        postxt = font1.render('(' + str(x) + ',' + str(y)+')',True,(255, 51, 153))
        #screen.blit(postxt, (x - 50, y - 50))
        #pygame.draw.rect(screen, (255, 51, 153), [x-5, y-5, 10, 10])
        #배관 관련 코드
        for i in range(3):
            if not game_over:
                if pipe_move_mode:
                    pipey[i] += move_dir[i]
                #배관 왼쪽으로 이동
                if not pipe_stop:
                    pipex[i] -= pipe_base_speed + pipe_increase_speed * (score >= change_score)
            
            #배관이 왼쪽 화면 밖으로 나갔다면 점수 + 1 하고 화면 오른쪽으로 보내기
            if pipex[i] <= 0 - pipew:
                pipex[i] = 1280 + pipew
                pipey[i] = random.randint(720/2, 720/2 + 300)
                score += 1

            if lr_rev_mode and not boss_mode:
                if pipex[i] >= 1280 + pipew:
                    pipex[i] = 0 - pipew
                    pipey[i] = random.randint(720 / 2, 720 / 2 + 300)
                    if pipey[i] <= 430:
                        move_dir[i] = -0.8
                    else:
                        move_dir[i] = 0.8
                    score += 1

            # 배관 그리기
            pipe_color = (0, 255, 0)
            if score >= change_score:
                pipe_color = (100, 30, 30)
            
            #배관 히트박스 그리기
            """
            pygame.draw.rect(screen, pipe_color, [pipex[i] - pipew / 2, pipey[i] - 720 / 2 - 350, pipew, pipeh])
            pygame.draw.rect(screen, back_color, [pipex[i] - pipew / 2 + 5, pipey[i] - 720 / 2 - 350 + 5, pipew - 10, pipeh - 10])
            pygame.draw.rect(screen, pipe_color, [pipex[i] - pipew / 2, pipey[i] + 100, pipew, pipeh])
            pygame.draw.rect(screen, back_color, [pipex[i] - pipew / 2 + 5, pipey[i] + 105, pipew - 10, pipeh - 10])
            """

            #배관 그리기
            if score >= change_score:
                screen.blit(tree1_img, (pipex[i] - pipe_img_w / 2, pipey[i] - 720 / 2 - 350))
                screen.blit(tree_img, (pipex[i] - pipe_img_w / 2, pipey[i] + 50))
            else:
                screen.blit(pipe_img, (pipex[i] - pipe_img_w / 2, pipey[i] - 720 / 2 - 350))
                screen.blit(pipe1_img, (pipex[i] - pipe_img_w / 2, pipey[i] + 50))
            
            postxt = font1.render('(' + str(pipex[i]) + ',' + str(pipey[i])+')',True,(255, 51, 153))

            #screen.blit(postxt, (pipex[i] - 40, pipey[i] - 30))

            #파이프 좌표 중심 그리기
            #pygame.draw.rect(screen, (255, 51, 153), [pipex[i]-5, pipey[i]-5, 10, 10])

            #충돌했다면 게임 오버를 True로 설정
            if collide(x - w / 2, y - h / 2, w, h, pipex[i] - pipew / 2, pipey[i] - 720 / 2 - 350, pipew, pipeh) or\
                collide(x - w / 2, y - h / 2, w, h, pipex[i] - pipew / 2, pipey[i] + 100, pipew, pipeh) or\
                y < 0 or y > 720:
                game_over = True

        if boss_mode:
            if collide(x, y, w, h, boss_x - 1280 + 400 + mouth_x, boss_y+150/2 + 25, 1280, 100):
                game_over = True
            if boss_x != 0 and not game_over:
                boss_x += 1
            else:
                if fire == 0 and not game_over:
                    if boss_y != ty:
                        boss_y += 20 if boss_y < ty else -20
                        if abs(boss_y - ty) < 20:
                            boss_y = ty
                        if boss_y == ty:
                            fire = 1
                    elif not game_over:
                        fire = 1
                elif not game_over:
                    if fire == 1:
                        mouth_x += 40
                        if mouth_x == 1280 - 400:
                            fire = 2
                    else:
                        if mouth_x > 1280 - 500:
                            mouth_x -= 1
                        else:
                            mouth_x -= 30
                            if mouth_x == 0:
                                ty = random.randint(10, 47) * 10
                                fire = 0
                                score += 1

            screen.blit(mouth_img, (boss_x - 1280 + 400 + mouth_x, boss_y+150/2))
            screen.blit(face_img, (boss_x, boss_y))

        #점수 표시
        score_color = (0, 0, 0)
        if score >= change_score:
            score_color = (255,255,255)
        scoretxt = font1.render('Score: ' + str(score),True,score_color)
        high_score = max(high_score, score)
        screen.blit(scoretxt, (10, 10))
        highscoretxt = font1.render('High Score: ' + str(high_score),True,score_color)
        screen.blit(highscoretxt, (10, 40))
        
        #게임 오버가 True라면 화면 가운데에 Game Over!표시 하고 게임을 정지 한다.
        if game_over:
            screen.blit(game_over_img, (0, 0))
            if first_game_over :
                mawang_bgm.stop()
                bgm.stop()
                mySound2.play()
                first_game_over = False
        
    elif is_setting_mode:
        screen.blit(background_img[background_setting], (0, 0))
        txt = font1.render('Click To Change Background',True,(0, 0, 0))
        screen.blit(txt, (1280/2-150, 20))
        screen.blit(back_img, (10, 10))
    
    else:
        screen.blit(background_img[background_setting], (0, 0))
        highscoretxt = font1.render('High Score: ' + str(high_score),True,(0, 0, 0))
        screen.blit(highscoretxt, (10, 10))
        screen.blit(setting_img, (1100, 600))
        screen.blit(title_img[background_setting], (1280/2-320, 720/2-280))
        screen.blit(gamestart_img[background_setting], (1280/2-150, 400))

    pygame.display.update()

# 2초 기다리고 게임을 끈다.
pygame.time.delay(2000)
sys.exit()
