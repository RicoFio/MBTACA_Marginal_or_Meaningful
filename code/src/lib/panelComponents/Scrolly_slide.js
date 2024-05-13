import { writable } from 'svelte/store';

function createObserverStore() {
    const { subscribe, set, update } = writable({
        isVisible: false,
        observer: null,
        timeout: null
    });

    const startObservation = (timeout_time=5000) => {
        update(state => {
            // Disconnect previous observers and clear timeouts
            if (state.observer) {
                state.observer.disconnect();
            }
            if (state.timeout) {
                clearTimeout(state.timeout);
                state.timeout = null;
            }

            // Setup a new observer
            state.observer = new IntersectionObserver(entries => {
                const [entry] = entries;
                if (entry.isIntersecting) {
                    state.timeout = setTimeout(() => {
                        update(innerState => ({ ...innerState, isVisible: true }));
                    }, 3000);
                }
            }, {
                root: document.querySelector('.slide'),
                threshold: 0.5
            });

            const target = document.querySelector('.slide > p:first-of-type');
            if (target) {
                state.observer.observe(target);
            }

            return state;
        });
    };

    const resetVisibility = () => {
        update(state => {
            state.isVisible = false;
            return state;
        });
    };

    const cleanUp = () => {
        update(state => {
            if (state.observer) {
                state.observer.disconnect();
            }
            if (state.timeout) {
                clearTimeout(state.timeout);
            }
            return { ...state, observer: null, timeout: null, isVisible: false };
        });
    };

    return { subscribe, startObservation, resetVisibility, cleanUp };
}

export const observerStore = createObserverStore();
