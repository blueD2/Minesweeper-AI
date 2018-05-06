# config.py

# configuration for game
board = dict(
    width               = 10,
    height              = 10,
    bombs               = 10,
)

#configuration for neural net
nnet = dict(
    n_inputs            = 24,
    n_h_layers          = 2,
    n_h_neurons0        = 15,
    n_h_neurons1        = 8,
    n_outputs           = 1,
)

#configuration for genetic algorithm
ga = dict(
    n_gens              = 100,
    pop_size            = 100,
    mutpb               = 0.3,
    cxpb                = 0.3,
)


