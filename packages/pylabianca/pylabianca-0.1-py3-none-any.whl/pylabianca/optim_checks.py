def _compute_spike_rate_numpy2(times, trials, limits, n_trials, winlen=0.25,
                               step=0.05):
    halfwin = winlen / 2
    epoch_len = limits[1] - limits[0]
    n_steps = int(np.floor((epoch_len - winlen) / step + 1))

    fr_tstart = limits[0] + halfwin
    fr_tend = limits[1] - halfwin + step * 0.001
    times = np.arange(fr_tstart, fr_tend, step=step)
    frate = np.zeros((n_trials, n_steps))

    n_epochs = event_times.shape[0]
    this_epo = trials[0]
    trilims = group(trials, diff=True)[:, 1]
    trilims = np.concatenate([[0], lims, len(trials)])

    for tridx in range(len(trilims) - 1):
        # find trials
        tms = times[trilims[tridx]:trilims[tridx + 1]]
        trial = trials[trilims[tridx]]

        # approach 1: compare with numpy array of window limits
        # approach 2: compare in a smarter way


def _select_spikes_twin(times, trials, tmin, tmax):
    msk = (times >= tmin) & (times < tmax)
    return times[msk], trials[msk]


def _old_times_trimming():
    # TODO: it makes more sense to change times to be between current
    #       time labels, than to asymmetrically trim the time labels?
    if (len(win_time) - 1) % 2 == 0:
        trim1 = int((len(win_time) - 1) / 2)
        trim2 = trim1
    else:
        trim1 = int((len(win_time) - 1) / 2)
        trim2 = trim1 + 1