from datetime import datetime
import torch
import numpy as np
from ppo import PPO
import wandb
import os
from gym_grid.grid_env import GridEnv

################################### Training ###################################
def train():
    # print("initialize Wandb")
    os.environ["WANDB_MODE"] = "online"
    os.environ["WANDB_API_KEY"] = "cc"
    user = "cc"
    project = "XPlane11"
    display_name = "Astar&RL_Training_PPO_6"
    wandb.init(entity=user, project=project, name=display_name)
    print("============================================================================================")
    has_continuous_action_space = False  # continuous action space; else discrete
    max_ep_len = 150  # max timesteps in one episode
    max_training_timesteps = int(3e6)  # break training loop if timeteps > max_training_timesteps
    print_freq = 1  # print avg reward in the interval (in num timesteps)
    log_freq = max_ep_len * 2  # log avg reward in the interval (in num timesteps)
    save_model_freq = int(1e5)  # save model frequency (in num timesteps)
    action_std = 0.6  # starting std for action distribution (Multivariate Normal)
    action_std_decay_rate = 0.05  # linearly decay action_std (action_std = action_std - action_std_decay_rate)
    min_action_std = 0.1  # minimum action_std (stop decay after action_std <= min_action_std)
    action_std_decay_freq = int(2.5e5)  # action_std decay frequency (in num timesteps)
    #####################################################
    ################ PPO hyperparameters ################
    update_timestep = 4000  # update policy every n timesteps
    K_epochs = 20  # update policy for K epochs in one PPO update
    eps_clip = 0.2  # clip parameter for PPO
    gamma = 0.99  # discount factor
    lr_actor = 0.0003  # learning rate for actor network
    lr_critic = 0.001  # learning rate for critic network
    random_seed = 0  # set random seed if required (0 = no random seed)
    #####################################################
    # state shape = 73 * 38 # continuous
    # action: 8 # Multidiscrete
    env_name = "Astar-RL"
    env = GridEnv(randomWalls=False, timeStep=250)
    state_dim = 73 * 38

    # action space dimension
    if has_continuous_action_space:
        action_dim = env.action_space.shape[0]
    else:
        action_dim = env.action_space


    log_dir = "PPO_logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_dir = log_dir + '/' + env_name + '/'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    #### get number of log files in log directory
    run_num = 0
    current_num_files = next(os.walk(log_dir))[2]
    run_num = len(current_num_files)

    #### create new log file for each run
    log_f_name = log_dir + '/PPO_' + env_name + "_log_" + str(run_num) + ".csv"

    print("current logging run number for " + env_name + " : ", run_num)
    print("logging at : " + log_f_name)
    #####################################################

    ################### checkpointing ###################
    run_num_pretrained = 0  #### change this to prevent overwriting weights in same env_name folder

    directory = "PPO_preTrained"
    if not os.path.exists(directory):
        os.makedirs(directory)

    directory = directory + '/' + env_name + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    checkpoint_path = directory + "PPO_{}_{}_{}.pth".format(env_name, random_seed, run_num_pretrained)


    if random_seed:
        print("--------------------------------------------------------------------------------------------")
        print("setting random seed to ", random_seed)
        torch.manual_seed(random_seed)
        env.seed(random_seed)
        np.random.seed(random_seed)
    #####################################################
    # initialize a PPO agent
    ppo_agent = PPO(state_dim, action_dim, lr_actor, lr_critic, gamma, K_epochs, eps_clip, has_continuous_action_space, action_std)
    # track total training time
    start_time = datetime.now().replace(microsecond=0)
    # printing and logging variables
    print_running_reward = 0
    print_running_episodes = 0
    log_running_reward = 0
    log_running_episodes = 0
    time_step = 0
    i_episode = 0
    # training loop
    episodeRewards = []
    while time_step <= max_training_timesteps:
        state = env.reset()
        current_ep_reward = 0
        timestep = 0
        done = False
        while not done:
            # print("episode: {} timestep: {} update num: {}".format(i_episode, timestep, time_step//update_timestep))
            # select action with policy
            action = ppo_agent.select_action(state)
            state, reward, done, _ = env.step(action)
            env.render()
            # saving reward and is_terminals
            ppo_agent.buffer.rewards.append(reward)
            ppo_agent.buffer.is_terminals.append(done)
            time_step += 1
            timestep += 1
            current_ep_reward += reward
            # update PPO agent
            if time_step % update_timestep == 0:
                print("!!update!!")
                ppo_agent.update()
            # if continuous action space; then decay action std of ouput action distribution
            if has_continuous_action_space and time_step % action_std_decay_freq == 0:
                ppo_agent.decay_action_std(action_std_decay_rate, min_action_std)

            # # save model weights
            # if time_step % save_model_freq == 0:
            #     print("--------------------------------------------------------------------------------------------")
            #     print("saving model at : " + checkpoint_path)
            #     ppo_agent.save(checkpoint_path)
            #     print("model saved")
            #     print("Elapsed Time  : ", datetime.now().replace(microsecond=0) - start_time)
            #     print("--------------------------------------------------------------------------------------------")

            # break; if the episode is over
            if done:
                print(print_running_episodes, timestep, done)
                break

        episodeRewards.append(current_ep_reward)
        print_running_reward += current_ep_reward
        print_running_episodes += 1
        print("episode reward: {} last 10 ep. mean: {}".format(episodeRewards[-1], np.mean(episodeRewards[-10:])))
        wandb.log({"episodeReward": current_ep_reward, "episode":i_episode})

        log_running_reward += current_ep_reward
        log_running_episodes += 1

        i_episode += 1


if __name__ == '__main__':
    train()






