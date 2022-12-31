from gym_grid.grid_env import GridEnv

def main():
    render = True
    env = GridEnv(randomWalls=True, timeStep=250)
    for episode in range(1000):
        done = False
        state = env.reset()
        while not done:
            action = env.player.selectAction()
            state, reward, done, _ = env.step(action)

            if render:
                env.render()


    env.close()

if __name__ == "__main__":
    main()