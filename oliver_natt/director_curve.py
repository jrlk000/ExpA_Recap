import numpy as np
import matplotlib as mpl
import matplotlib.animation
import matplotlib.pyplot as plt
import math
import logging

# ---- Logger ----
DEBUG = True
#Configuration
logging.basicConfig(
	level=logging.INFO,
	format='%(filename)s %(lineno)d - %(message)s'
)

#Create instance
logger = logging.getLogger("director_curve")

#Switch between logger levels
if DEBUG:
	logger.setLevel(logging.DEBUG)

#initial values defining start position, angle, velocity for hunter and target
phy = 0

v_abs_hunter = 2 #[m/s²]

#initial velocities
dr_dt_target = 1 #[m/s] translation
d_phy_dt_target = 0 #[rad/s] rotation

#initial positions
r0_target = np.array([0, 0], dtype=float) #[m]
r0_hunter = np.array([0, 10], dtype=float) #[m]

v0_target = dr_dt_target * np.array([math.cos(phy), math.sin(phy)]) + d_phy_dt_target * np.array([-math.sin(phy), math.cos(phy)], dtype=float)
v0_hunter = v_abs_hunter * (r0_target-r0_hunter)/np.linalg.norm(r0_target-r0_hunter)

#store initial distance
distances = [np.linalg.norm(r0_target-r0_hunter)]

#positions
target_positions = [r0_target]
hunter_positions = [r0_hunter]

#hunter vel and acc
#last_hunter_velocities = np.zeros((2, 2)) #just stores the needed velocities for the differential quotient
hunter_velocities = [np.zeros((2, ), dtype=float)]
hunter_accelerations = [np.zeros((2, ))]

#loop to get the position, acceleration, relative distance values of the hunter
dt = 1e-3
time_interval = [dt]
while not math.isclose(distances[-1], 0, abs_tol=1e-1):
	#compute new velocity vector for the hunter
	v_hunter = v_abs_hunter * (target_positions[-1] - hunter_positions[-1]) / distances[-1]
	hunter_velocities.append(v_hunter)

	#last_hunter_velocities[0] = last_hunter_velocities[1]
	#last_hunter_velocities[1] = v_hunter

	#compute new position of hunter and target
	hunter_positions.append(hunter_positions[-1] + v_hunter * dt) #why do we not use the acceleration in the quadratic term in this step?
	target_positions.append(target_positions[-1] + v0_target * dt)

	#acceleration - the speed value stays constant but the direction changes dynamically so the acceleration isn't zero
	hunter_accelerations.append((hunter_velocities[-1] - hunter_velocities[-2]) / dt)

	#update values
	distances.append(np.linalg.norm(hunter_positions[-1] - target_positions[-1]))

	#time inrcrement
	time_interval.append(time_interval[-1]+dt)

# ---- plot the computed values ----
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 8))

# x over hunter
pos_hunter = np.array(hunter_positions, dtype=float)
x_pos_hunter = pos_hunter[:, 0]
y_pos_hunter = pos_hunter[:, 1]

ax1.set_title("x over y of hunter.")
ax1.set_xlabel("x [m]")
ax1.set_ylabel("y [m]")

ax1.plot(x_pos_hunter, y_pos_hunter, color="blue")
ax1.legend(["hunter pos 2D."])

bbox_ax1 = ax1.get_position() #returns a bounding box
#ax1.set_position([0, 0, pos_ax1.width, pos_ax1.height])
logger.debug(f"x_val, y_val, width, height: {bbox_ax1.bounds}")


#relative distance over t
ax2.set_title("dist. over time.")
ax2.set_xlabel("time [s]")
ax2.set_ylabel("dist [m]")

ax2.plot(time_interval, distances, color="red")
ax2.legend(["Dist."])

plt.show()

#animation
"""plot_curve_hunter, = ax3.plot([], [])
plot_hunter, = ax3.plot([], [], 'o', color='blue')
plot_target, = ax3.plot([], [], 'o', color='red')

style = mpl.patches.ArrowStyle.Simple(head_length=6, head_width=3)

pfeil_v = mpl.patches.FancyArrowPatch((0, 0), (0, 0), color='red', arrowstyle=style)
pfeil_a = mpl.patches.FancyArrowPatch((0, 0), (0, 0), color='black', arrowstyle=style)

ax3.add_patch(pfeil_v)
ax3.add_patch(pfeil_a)

# ---- update the plot for animation ----
def update(n: int):
	
	Update the axis.

	Args:

	Returns:

	
	pfeil_v.set_positions(hunter_positions[n], hunter_positions[n] + hunter_velocities[n])
	pfeil_a.set_positions(hunter_positions[n], hunter_positions[n] + hunter_accelerations[n])

	#set the position of the hunter and the target in plot.
	plot_hunter.set_data(hunter_positions[n])
	plot_target.set_data(target_positions[n])
	plot_curve_hunter.set_data(hunter_positions[:n+1, 0] ,hunter_positions[:n+1, 1])
	return plot_curve_hunter, plot_hunter, plot_target, pfeil_v, pfeil_a

ani = mpl.animation.FuncAnimation(fig, update, frames=len(time_interval), interval=30, blit=True)

#acceleration over t
plt.show()"""

"""while not math.isclose(np.linalg.norm(r), 0, abs_tol=1e-1):
	logger.debug("Entered loop.")
	logger.debug(f"positions: chaser: {positions_chaser[-1]}, target: {positions_chaser[-1]}")
	logger.debug(f"norm of relative vector: {np.linalg.norm(r)}")
	counter += 1
	#compute an acceleration for the chaser based on position difference in last step
	new_acceleration = (np.linalg.norm(r) * np.array([math.cos(theta), math.sin(theta)], dtype=float))

	#compute the resulting velocity vector for chaser
	#new_velocity = new_velocity[-1] + new_acceleration * dt
	velocity_values_chaser.append(dt * new_acceleration)

	#compute new positions
	new_pos_chaser = positions_chaser[-1] + v_chaser_0 * dt + new_acceleration/2 * dt**2
	new_pos_target = positions_target[-1] + v_target_0 * dt

	logger.debug(v_target_0)
	logger.debug(new_pos_target)
	logger.debug(new_pos_chaser)

	#update relative vector
	r = new_pos_chaser - new_pos_target
	logger.debug(f"Vector shape of relative vector: rx: {r[0]}, ry: {r[1]}.")

	#colloect new positions
	positions_chaser.append(new_pos_chaser)
	positions_target.append(new_pos_target)


logger.debug(f"Left the loop after a count of: {counter}.")"""

#allows just a linear or no acceleration but no adaptable one
"""end_times = []
for k in (0, 1):
	if v_relative[k] ** 2 - 4 * r[k] * v_abs_chaser >= 0:
		end_times.append((-v_relative[k] + math.sqrt(v_relative[k] ** 2 - 4 * r[k] * v_abs_chaser)) / (2 * v_abs_chaser))
		end_times.append((-v_relative[k] - math.sqrt(v_relative[k] ** 2 - 4 * r[k] * v_abs_chaser)) / (2 * v_abs_chaser))""""""

logger.debug(f"Time interval end candidates: {end_times}.")
time_vector = np.linspace(0, max(end_times), 100).reshape(100, 1)

# ------------------------------------

s_chaser = (v_abs_chaser * time_vector ** 2) / 2 + (time_vector * v_chaser) + r0_chaser
s_target = (time_vector * v_target_0) + r0_target
logger.debug(f"End of time interval: {time_vector[-1]}")
logger.debug(f"Positions of chaser: {s_chaser[-1]} and target: {s_target[-1]} ")

if not np.allclose(s_chaser[-1], s_target[-1]):
	raise ValueError("The end position of target and chaser differ: target: {}, chaser: {}.".format(s_target[-1], s_chaser[-1]))"""

#fig, (ax1) = plt.subplots(1, 1)

#plot s_chaser_x, over time
"""ax1.set_title("s_chaser_x over time")
ax1.plot(s_chaser[:0], time_vector.reshape(time_vector.shape[1], time_vector.shape[0]), color="blue")
ax1.set_xlabel("x-Position [m]")
ax1.set_ylabel("Time [s]")"""




#plt.show()