from planner import *

############################


goal_state = State(['stomach_full','at_kitchen','has_recipe'])
init_state = State(['not_snowing','has_no_money','has_recipe'])
get_cash = Action('get_cash',
					preconditions = ['has_no_money'], 
					add_list = ['has_money'], 
					delete_list = ['has_no_money'])

drive_to_store = Action('drive_to_store',
					preconditions = ['has_money','not_snowing'], 
					add_list = ['at_store'], 
					delete_list = ['not_snowing'])

buy_items = Action('buy_items',
					preconditions = ['has_money','at_store'], 
					add_list = ['has_vegetables','has_meat','has_rice','has_no_money'], 
					delete_list = ['has_money'])

drive_home = Action('drive_home',
					preconditions = ['at_store'], 
					add_list = ['at_home'], 
					delete_list = ['at_store'])

go_to_kitchen = Action('go_to_kitchen',
					preconditions = ['at_home','has_vegetables','has_meat','has_rice'], 
					add_list = ['at_kitchen'], 
					delete_list = [])

cook_food = Action('cook_food',
					preconditions = ['at_kitchen','has_recipe'], 
					add_list = ['food_cooked'], 
					delete_list = ['has_vegetables','has_meat','has_rice'])

eat_food = Action('eat_food',
					preconditions = ['food_cooked'], 
					add_list = ['stomach_full'], 
					delete_list = ['food_cooked'])

#get_fuel = Action('get_fuel',
					#preconditions = ['has_no_fuel'], 
					#add_list = ['has_fuel'], 
					#delete_list = ['has_no_fuel'])

actions = [get_cash, drive_to_store, buy_items, drive_home, go_to_kitchen, cook_food, eat_food]

############################
### Test the heuristic

state0 = State(['food_cooked','at_home','at_kitchen','has_recipe'])
state1 = State(['has_recipe','at_home','has_vegetables','has_meat','has_rice'])
state2 = State(['at_home','at_kitchen','has_recipe','has_no_money'])
state3 = State(['at_kitchen','has_recipe','has_money','not_snowing'])
state4 =  State(['has_recipe','has_money','not_snowing'])
state5 = State(['at_store','has_recipe','has_money'])
state6 = init_state

tests = [state0, state1, state2, state3, state4, state5, state6]



print("TESTING compute_heuristic")

the_planner = Planner()
for n, state in enumerate(tests):
	h = the_planner.compute_heuristic(state, goal_state, actions)
	print("TEST", n, "h=", h)

#############################
### Run planner

print("TESTING astar")

for n, state in enumerate(tests):
	print("TEST", n)
	the_planner = Planner()
	the_planner.initial_state = state
	the_planner.goal_state = goal_state
	the_planner.actions = actions
	plan, closed = the_planner.astar(state, goal_state, actions)
	for act in plan:
		print(act.name)
	print("states visited", len(closed))
