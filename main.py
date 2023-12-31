import requirements
import pygame
import screens, events, functions, interface
from settings import Settings
from squares import Squares
import AI_player

round = 0
generation = 0
points_log = []
score_log = []

mutation_rate = 0.1
top_percentage = 0.4
population_size = 80
generations = 20
trials = 5

def run():
    # initializations
    pygame.init()
    status = functions.Status()
    st = Settings()

    screen = pygame.display.set_mode(st.screen_size)
    pygame.display.set_caption(st.screen_name)

    func = functions.Fucntions(st, screens.get_func_surface(screen, st))
    sqs = Squares(st, status, screens.get_sqs_surface(screen, st))

    AI = AI_player.AI()
    # main loop
    while True:
        pygame.display.flip()
        events.check_events(sqs, status, AI)

        if status.is_game_active():
            if sqs.update():
                screens.update_screen(screen, sqs, func, status, st)
        elif status.is_game_over():

            points_log.append(status.points)
            score_log.append(status.score)

            print("Score: ", status.score)
            return status.score
        
        elif status.is_game_new():
            interface.start(screen, st)
        elif status.is_game_renew():
            AI_mode = status.new_AI
            status.refresh()
            status.game_status = status.ACTIVE
            sqs = Squares(st, status, screens.get_sqs_surface(screen, st))
            st = Settings()
            if AI_mode:
                status.AI = True
                sqs.st.adjust_for_AI()

            status.AI = True
            status.new_AI = True
            sqs.st.adjust_for_AI()
            
        else:
            raise RuntimeError # this should never happen


if __name__ == "__main__":
    requirements.check()
    AI_player.genetic_main()


