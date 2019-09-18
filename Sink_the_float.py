#Sink the float

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors

import time

militime = lambda: time.time() * 1000

#Define map colors  
levels = [-1, 0, 1, 2, 3]
colors = ['b', 'y', 'g' , 'r']

cmap, norm = matplotlib.colors.from_levels_and_colors(levels, colors)

######################################################
#													 #
# 				 FUNCIONES GENERALES				 #
#													 #
######################################################


def read_map(name):
	#Read the excel file
	df = pd.read_excel('%s.xlsx' % name)
	grid = df.as_matrix()

	return grid

def plot_map(grid):
	#Plot the excel file as matrix to account for the map
	plt.imshow(grid)
	plt.show()

def contador_celdas(grid):

	row = grid.shape[0]
	cols = grid.shape[1]

	#0 -> celda agua
	#1 -> celda barco
	#2 -> celda agua tocada
	#3 -> celda barco tocado

	celdas_agua = 0
	celdas_barco = 0
	celdas_agua_tocada = 0
	celdas_barco_tocado = 0

	for i in range(row):
		for j in range(cols):

			if grid[i][j] == 0:
				celdas_agua += 1

			elif grid[i][j] == 1:
				celdas_barco += 1

			elif grid[i][j] == 2:
				celdas_agua_tocada += 1

			else:
				celdas_barco_tocado += 1

	return celdas_agua, celdas_barco, celdas_agua_tocada, celdas_barco_tocado

def validate_cell(grid, x, y):

	for i in [(1, 0), (-1, 0), (0, 1), (0, -1)]:

		try:

			x_new = x + i[0]
			y_new = y + i[1]

			if grid[y_new][x_new] == 3:
				return False

		except:
			pass

	return True
			

######################################################
#													 #
# 				    ALGORITMOS						 #
#													 #
######################################################

def sweep(grid):

	'''
		Explicar algoritmo barrido
	'''
	
	row = grid.shape[0]
	cols = grid.shape[1]

	ship_cells = np.sum(grid)

	ship_cells_t = [ship_cells]
	iteration = 0

	for i in range(row):
		for j in range(cols):

			iteration += 1

			#print('Iteration %i with %i cell ships' % (iteration, ship_cells))

			if grid[i][j] == 1:
				grid[i][j] = 0
			
			ship_cells = np.sum(grid)
			ship_cells_t.append(ship_cells)

			if ship_cells == 0:
				break

	return iteration, ship_cells_t

def random_no_memory(grid):

	'''
		Explicar algoritmo random sin memoria
	'''

	ship_cells = np.sum(grid)
	iteration = 0

	rows = grid.shape[0]
	cols = grid.shape[1]

	ship_cells_t = [ship_cells]

	while ship_cells > 0:

		iteration += 1

		#print('Iteration %i with %i cell ships' % (iteration, ship_cells))
		
		x = np.random.randint(cols)
		y = np.random.randint(rows)

		if grid[y][x] == 1:
			grid[y][x] = 0
			
		ship_cells = np.sum(grid)

		ship_cells_t.append(ship_cells)

	return iteration, ship_cells_t

def random_with_memory(grid):

	'''
		Explicar algoritmo random con memoria
	'''
	
	ship_cells = np.sum(grid)
	iteration = 0
	cells_visited = []

	rows = grid.shape[0]
	cols = grid.shape[1]

	ship_cells_t = [ship_cells]

	while ship_cells > 0:

		iteration += 1

		#print('Iteration %i with %i cell ships' % (iteration, ship_cells))
				
		x = np.random.randint(cols)
		y = np.random.randint(rows)

		cell = (y, x)

		while cell in cells_visited:
			
			x = np.random.randint(cols)
			y = np.random.randint(rows)

			cell = (y, x)

		cells_visited.append(cell)

		if grid[y][x] == 1:
			grid[y][x] = 0
		
		ship_cells = np.sum(grid)
		ship_cells_t.append(ship_cells)	

	return iteration, ship_cells_t

def human(grid):

	'''
		Explicar algoritmo
	'''
	
	celdas_agua, celdas_barco, celdas_agua_tocada, celdas_barco_tocado = contador_celdas(grid)

	iteration = 0

	rows = grid.shape[0]
	cols = grid.shape[1]

	ship_cells_t = [celdas_barco]

	while celdas_barco > 0:
				
		x = np.random.randint(cols)
		y = np.random.randint(rows)

		boolean = validate_cell(grid, x, y)

		while grid[y][x] > 1 or boolean == False:
			
			x = np.random.randint(cols)
			y = np.random.randint(rows)

			boolean = validate_cell(grid, x, y)


		x_init = x
		y_init = y

		############ celda nueva escogida ###########

		if grid[y][x] == 1: #Si la celda es un barco, cambiar a barco tocado y seguir disparando alrededor (el for de dentro)

			iteration += 1

			grid[y][x] = 3

			#print('Iteration %i with %i cell ships' % (iteration, celdas_barco))
			celdas_agua, celdas_barco, celdas_agua_tocada, celdas_barco_tocado = contador_celdas(grid)
			ship_cells_t.append(celdas_barco)

			contador = 0
			changed_dir = False

			directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

			for i in range(4): #Ir disparando en los 4 ejes (x+,x-,y+,y-)

				if i == 1 and contador > 0: #Si has ido en x+ y has tocado barco, ve en el otro sentido pero misma direccion
					i += 1 

					changed_dir = True

				elif i == 3 and contador > 0:
					break

				if celdas_barco == 0:
					break

				repeat = True

				x = x_init
				y = y_init

				contador = 0

				while repeat == True:

					if celdas_barco == 0:
						break

					x += directions[i][0] 
					y += directions[i][1]

					try:

						if grid[y][x] == 0:

							repeat = False

							if changed_dir == False:

								grid[y][x] = 2								

								iteration += 1

								#print('Iteration %i with %i cell ships' % (iteration, celdas_barco))
								celdas_agua, celdas_barco, celdas_agua_tocada, celdas_barco_tocado = contador_celdas(grid)
								ship_cells_t.append(celdas_barco)

						elif grid[y][x] == 1:

							grid[y][x] = 3

							iteration += 1

							contador += 1

							#print('Iteration %i with %i cell ships' % (iteration, celdas_barco))
							celdas_agua, celdas_barco, celdas_agua_tocada, celdas_barco_tocado = contador_celdas(grid)
							ship_cells_t.append(celdas_barco)

						else:
							repeat = False

					except:
						break


		elif grid[y][x] == 0: #Si la celda es agua, cambiar a agua tocada

			iteration += 1

			grid[y][x] = 2

			#print('Iteration %i with %i cell ships' % (iteration, celdas_barco))
			celdas_agua, celdas_barco, celdas_agua_tocada, celdas_barco_tocado = contador_celdas(grid)
			ship_cells_t.append(celdas_barco)

	return iteration, ship_cells_t

######################################################
#													 #
# 				    	JUEGOS						 #
#													 #
######################################################

def game_sweep():

	mapa = read_map('grid')

	#plot_map(mapa)

	t0 = militime()

	finish_iter , ship_cells_t = sweep(mapa)

	tf = militime()

	time_elapsed = tf - t0

	#plot_map(mapa)

	#Estudio

	iters_list = np.linspace(1, len(ship_cells_t), len(ship_cells_t))

	plt.plot(iters_list, ship_cells_t, color='r', ls='--', marker='None')
	plt.text(100, 25, 'Computational time elapsed: %.2f ms' % time_elapsed)

	plt.title('Sweep performance %i its' % finish_iter)
	plt.xlabel('Iteraciones')
	plt.ylabel('Celdas no hundidas')

	plt.show()
	
def game_random_no_memory():

	#Leer mapa
	mapa = read_map('grid')	

	#Algoritmo
	t0 = militime()

	finish_iter , ship_cells_t = random_no_memory(mapa)

	tf = militime()

	time_elapsed = tf - t0

	print(time_elapsed)

	#plot_map(mapa)

	#Estudio
	iters_list = np.linspace(1, len(ship_cells_t), len(ship_cells_t))

	plt.plot(iters_list, ship_cells_t, color='r', ls='--', marker='')
	#plt.text(100, 25, 'Computational time elapsed: %.2f ms' % time_elapsed)

	plt.title('Random with no memory performance %i its' % finish_iter)
	plt.xlabel('Iteraciones')
	plt.ylabel('Celdas no hundidas')

	plt.show()

def game_random_with_memory():
	
	#Leer mapa
	mapa = read_map('grid')	

	#Algoritmo
	t0 = militime()

	finish_iter , ship_cells_t = random_with_memory(mapa)

	tf = militime()

	time_elapsed = tf - t0

	print(time_elapsed)

	#plot_map(mapa)

	#Estudio
	iters_list = np.linspace(1, len(ship_cells_t), len(ship_cells_t))

	plt.plot(iters_list, ship_cells_t, color='r', ls='--', marker='')
	#plt.text(100, 25, 'Computational time elapsed: %.2f ms' % time_elapsed)

	plt.title('Random with memory performance %i its' % finish_iter)
	plt.xlabel('Iteraciones')
	plt.ylabel('Celdas no hundidas')

	plt.show()

def game_human():
	
	#Leer mapa
	mapa = read_map('grid')	

	#Algoritmo
	t0 = militime()

	finish_iter , ship_cells_t = human(mapa)

	tf = militime()

	time_elapsed = tf - t0

	print(time_elapsed)

	#plot_map(mapa)

	#Estudio
	iters_list = np.linspace(1, len(ship_cells_t), len(ship_cells_t))

	plt.plot(iters_list, ship_cells_t, color='r', ls='--', marker='')
	#plt.text(100, 25, 'Computational time elapsed: %.2f ms' % time_elapsed)

	plt.title('Human performance %i its' % finish_iter)
	plt.xlabel('Iteraciones')
	plt.ylabel('Celdas no hundidas')

	plt.show()


######################################################
#													 #
# 				   		STUDIES						 #
#													 #
######################################################

def comparison():

	print('----------- Sweep method ----------')

	mapa = read_map('grid')

	t0 = militime()

	finish_iter_sweep , ship_cells_t_sweep = sweep(mapa)

	tf = militime()

	time_elapsed_sweep = tf - t0

	print('----------- Random No Memory method ----------')

	mapa = read_map('grid')

	t0 = militime()

	finish_iter_random , ship_cells_t_random = random_no_memory(mapa)

	tf = militime()

	time_elapsed_random = tf - t0

	print('----------- Random With Memory method ----------')

	mapa = read_map('grid')

	t0 = militime()

	finish_iter_random_memory , ship_cells_t_random_memory = random_with_memory(mapa)

	tf = militime()

	time_elapsed_random_memory = tf - t0

	print('----------- Human method ----------')

	mapa = read_map('grid')

	t0 = militime()

	finish_iter_human , ship_cells_t_human = human(mapa)

	tf = militime()

	time_elapsed_human = tf - t0

	#Time evolution plot
	x_sweep = np.arange(0, finish_iter_sweep + 1, 1)
	x_random = np.arange(0, finish_iter_random + 1, 1)
	x_random_memory = np.arange(0, finish_iter_random_memory + 1, 1)
	x_human = np.arange(0, finish_iter_human + 1, 1)

	plt.plot(x_sweep, ship_cells_t_sweep, color='r', label='Sweep')
	plt.plot(x_random, ship_cells_t_random, color='b', label='Random choice no memory')
	plt.plot(x_random_memory, ship_cells_t_random_memory, color='g', label='Random choice with memory')
	plt.plot(x_human, ship_cells_t_human, color='y', label='Human')

	plt.title('Method comparison')
	plt.xlabel('Iterations')
	plt.ylabel('N cell_ships')

	plt.legend()
	plt.show()

	#Barplot
	plt.figure(figsize=(10,6))

	plt.subplot(1, 2, 1)

	plt.bar([1], [finish_iter_sweep], color='r', label='Sweep')
	plt.bar([2], [finish_iter_random], color='b', label='Random choice no memory')
	plt.bar([3], [finish_iter_random_memory], color='g', label='Random choice with memory')
	plt.bar([4], [finish_iter_human], color='y', label='Human')

	ticks = [1, 2, 3, 4]
	labels= ['SW', 'RCNM', 'RCWM', 'H']

	plt.xticks(ticks, labels)

	plt.legend()

	#Barplot elapsed time

	plt.subplot(1, 2, 2)

	plt.bar([1], [time_elapsed_sweep], color='r', label='Sweep')
	plt.bar([2], [time_elapsed_random], color='b', label='Random choice no memory')
	plt.bar([3], [time_elapsed_random_memory], color='g', label='Random choice with memory')
	plt.bar([4], [time_elapsed_human], color='y', label='Human')

	ticks = [1, 2, 3, 4]
	labels= ['SW', 'RCNM', 'RCWM', 'H']

	plt.xticks(ticks, labels)

	plt.legend()
	plt.show()	

def average_random_memory(N):
	finish_iters = []

	for i in range(N):
		
		#Leer mapa
		mapa = read_map('grid')
		
		#Algoritmo
		finish_iter , ship_cells_t = random_with_memory(mapa)
		finish_iters.append(finish_iter)

	#Construct a list with the values of finish_iters < 94 (sweep performance for 'grid' map)
	finish_iters = np.array(finish_iters)

	outperform = len(finish_iters[finish_iters < 94])
	outperform_percentage = outperform / N * 100
	print('Outperforms: %i' % outperform, 'or', outperform_percentage, '%')

	avg = int(round(np.mean(finish_iters), 2))

	x = np.arange(1, N+1, 1)
	avg_arr = np.linspace(avg, avg, len(finish_iters))

	plt.subplot(1, 2, 1)

	plt.plot(x, finish_iters, color='b', label='Finish iter per game')
	plt.plot(x, avg_arr, color='r', label='Avg value: %i' % avg)

	plt.legend()
	plt.title('Average Random Choice With Memory')


	plt.subplot(1, 2, 2)

	plt.hist(finish_iters, density=True)

	plt.show()

def average_random(N):

	finish_iters = []

	for i in range(N):

		#Leer mapa
		mapa = read_map('grid')

		#Algoritmo
		finish_iter , ship_cells_t = random_no_memory(mapa)

		finish_iters.append(finish_iter)

	avg = int(round(np.mean(finish_iters), 2))

	x = np.arange(1, N+1, 1)
	avg_arr = np.linspace(avg, avg, len(finish_iters))

	plt.subplot(1,2,1)

	plt.plot(x, finish_iters, color='b', label='Finish iter per game')
	plt.plot(x, avg_arr, color='r', label='Avg value: %i' % avg)

	plt.legend()
	plt.title('Average Random Choice No Memory')

	plt.subplot(1, 2, 2)
	plt.hist(finish_iters, bins=25, density=True)
	plt.show()

def average_human(N):

	finish_iters = []

	for i in range(N):

		#Leer mapa
		mapa = read_map('grid')

		#Algoritmo
		finish_iter , ship_cells_t = human(mapa)

		finish_iters.append(finish_iter)

	avg = int(round(np.mean(finish_iters), 0))

	x = np.arange(1, N+1, 1)
	avg_arr = np.linspace(avg, avg, len(finish_iters))

	

	plt.subplot(1,2,1)

	plt.plot(x, finish_iters, color='b', label='Finish iter per game')
	plt.plot(x, avg_arr, color='r', label='Avg value: %i' % avg)

	plt.legend()
	plt.title('Average Human')

	plt.subplot(1, 2, 2)
	plt.hist(finish_iters, bins=25, density=True)
	plt.show()

def comparison_avg(N):

	finish_iters_random_memory = []
	finish_iters_random = []
	finish_iters_human = []

	print('---------- Sweep ----------')

	mapa = read_map('grid')

	finish_iter_sweep, ship_cells_t_sweep = sweep(mapa)

	print('---------- Random No Memory ----------')

	for i in range(N):

		#Leer mapa
		mapa = read_map('grid')

		#Algoritmo
		finish_iter, ship_cells_t = random_no_memory(mapa)

		finish_iters_random.append(finish_iter)

	print('---------- Random Memory ----------')

	for i in range(N):
		
		#Leer mapa
		mapa = read_map('grid')
		
		#Algoritmo
		finish_iter, ship_cells_t = random_with_memory(mapa)

		finish_iters_random_memory.append(finish_iter)

	print('---------- Human ----------')

	for i in range(N):

		#Leer mapa
		mapa = read_map('grid')

		#Algoritmo
		finish_iter, ship_cells_t = human(mapa)

		finish_iters_human.append(finish_iter)

	avg_sweep = finish_iter_sweep
	avg_random = int(round(np.mean(finish_iters_random), 0))
	avg_random_memory = int(round(np.mean(finish_iters_random_memory), 0))
	avg_human = int(round(np.mean(finish_iters_human), 0))

	#Comparacion quantitativa entre sweep (2º mejor) y humano (mejor)

	aumento_relativo = avg_sweep / avg_human * 100 - 100

	print('Sweep es un %.2f' % aumento_relativo, '% más ineficiente que el humano')

	#PLOTS

	plt.bar([1], [avg_sweep], color='r', label='Sweep')
	plt.bar([2], [avg_random], color='b', label='Random')
	plt.bar([3], [avg_random_memory], color='g', label='Random Memory')
	plt.bar([4], [avg_human], color='y', label='Human')

	ticks = [1, 2, 3, 4]
	labels = ['SW', 'RCNM', 'RCWM', 'H']

	plt.xticks(ticks, labels)

	plt.legend()
	plt.title('Comparison Average')

	plt.show()


######################################################
#													 #
# 				   CORRER JUEGOS					 #
#													 #
######################################################

#game_sweep()
#game_random_no_memory()
#game_random_with_memory()
#game_human()

######################################################
#													 #
# 				   COMPARACIÓN y ESTUDIOS			 #
#													 #
######################################################

numero = 1000

#comparison()
#average_random_memory(numero)
#average_random(numero)
#average_human(numero)

#comparison_avg(numero)