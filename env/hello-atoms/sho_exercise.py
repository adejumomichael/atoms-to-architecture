"""Week 1 warm-up: simple harmonic oscillator.
Compare analytical, Euler and velocity Verlet for energy and momentum.
Units: m = k = 1, so the period is 2*pi (about 6.283).
"""
import numpy as np
import matplotlib
#matplotlib.use("Agg")          # remove this line if you want plt.show() windows
import matplotlib.pyplot as plt

m, k = 1.0, 1.0


# ---------- Part A: single mass on a wall spring (energy test) ----------
x0, v0 = 1.0, 0.0


def energy1(x, v):
    return 0.5 * m * v**2 + 0.5 * k * x**2


def analytical(t):
    w = np.sqrt(k / m)
    x = x0 * np.cos(w * t) + (v0 / w) * np.sin(w * t)
    v = -x0 * w * np.sin(w * t) + v0 * np.cos(w * t)
    return x, v


def euler1(dt, n):
    x = np.empty(n + 1); v = np.empty(n + 1)
    x[0], v[0] = x0, v0
    for i in range(n):
        a = -k * x[i] / m
        x[i + 1] = x[i] + v[i] * dt
        v[i + 1] = v[i] + a * dt
    return x, v


def verlet1(dt, n):
    x = np.empty(n + 1); v = np.empty(n + 1)
    x[0], v[0] = x0, v0
    a = -k * x[0] / m                      # step 1: force at t=0, once only
    for i in range(n):
        v_half = v[i] + 0.5 * dt * a       # half-kick
        x[i + 1] = x[i] + dt * v_half      # drift
        a = -k * x[i + 1] / m              # NEW force at new position
        v[i + 1] = v_half + 0.5 * dt * a   # half-kick
    return x, v


# ---------- Part B: two masses joined by a spring, no wall (momentum test) ----------
L0 = 1.0


def force2(x):
    s = x[1] - x[0] - L0                   # extension of the spring
    f = k * s
    return np.array([f, -f])               # equal and opposite


def energy2(x, v):
    s = x[1] - x[0] - L0
    return 0.5 * m * np.sum(v**2) + 0.5 * k * s**2


def run2(method, dt, n):
    x = np.array([0.0, 1.5]); v = np.array([0.2, 0.0])
    X = np.empty((n + 1, 2)); V = np.empty((n + 1, 2))
    X[0], V[0] = x, v
    a = force2(x) / m
    for i in range(n):
        if method == "euler":
            x_new = x + v * dt
            v_new = v + (force2(x) / m) * dt
            x, v = x_new, v_new
        else:
            v_half = v + 0.5 * dt * a
            x = x + dt * v_half
            a = force2(x) / m
            v = v_half + 0.5 * dt * a
        X[i + 1], V[i + 1] = x, v
    return X, V


if __name__ == "__main__":
    dt, T = 0.05, 20.0
    n = int(round(T / dt))
    t = np.arange(n + 1) * dt

    # Part A
    xa, va = analytical(t)
    xe, ve = euler1(dt, n)
    xv, vv = verlet1(dt, n)
    Ea, Ee, Ev = energy1(xa, va), energy1(xe, ve), energy1(xv, vv)
    print("PART A  (dt=%.3f, %d steps, t=%.1f)" % (dt, n, T))
    print("  E0 analytical        :", Ea[0])
    print("  E_final Euler        :", Ee[-1], " ratio to E0:", Ee[-1] / Ea[0])
    print("  E_final Verlet       :", Ev[-1])
    print("  max|E-E0| Verlet     :", np.max(np.abs(Ev - Ea[0])))
    print("  Euler factor per step (1+dt^2):", 1 + dt**2,
          " -> after n steps:", (1 + dt**2) ** n)

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(t, Ea, label="analytical")
    ax.plot(t, Ee, label="Euler")
    ax.plot(t, Ev, "--", label="velocity Verlet")
    ax.set_xlabel("time"); ax.set_ylabel("total energy"); ax.legend()
    fig.tight_layout(); fig.savefig("sho_energy.png", dpi=130)

    # Part B
    print("\nPART B  (two masses, no wall)")
    fig2, (axp, axe) = plt.subplots(1, 2, figsize=(10, 4))
    for method in ("euler", "verlet"):
        X, V = run2(method, dt, n)
        P = m * V.sum(axis=1)
        E = np.array([energy2(X[i], V[i]) for i in range(n + 1)])
        print("  %-6s p0=%.6f  max|p-p0|=%.2e  E0=%.6f  E_final=%.6f"
              % (method, P[0], np.max(np.abs(P - P[0])), E[0], E[-1]))
        axp.plot(t, P, label=method)
        axe.plot(t, E, label=method)
    axp.set_title("total momentum"); axp.set_xlabel("time"); axp.legend()
    axe.set_title("total energy"); axe.set_xlabel("time"); axe.legend()
    fig2.tight_layout(); fig2.savefig("two_mass.png", dpi=130)

    # Step 4: dt scaling, fixed total time
    print("\nSTEP 4  Verlet energy error vs dt (T=%.1f)" % T)
    prev = None
    for d in (0.1, 0.05, 0.025):
        nn = int(round(T / d))
        xx, vv_ = verlet1(d, nn)
        dev = np.max(np.abs(energy1(xx, vv_) - 0.5))
        ratio = "" if prev is None else "  ratio to previous: %.2f" % (prev / dev)
        print("  dt=%.3f  max|E-E0|=%.3e%s" % (d, dev, ratio))
        prev = dev

    plt.show()