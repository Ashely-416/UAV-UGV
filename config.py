config = {
    'algorithm': 'A3C',  # Switch between 'A3C' and 'DDPG'
    'num_episodes': 100,
    'num_steps': 100,
    'targets': [
        {'x': 10, 'y': 10, 'type': 'static'},
        {'x': 20, 'y': 20, 'type': 'random'},
        {'x': 30, 'y': 30, 'type': 'a_star'}
    ]
}
