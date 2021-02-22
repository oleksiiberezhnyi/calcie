var type_of_construction_wall = Object();

type_of_construction_wall['Несуча стіна'] = 'Опирання з однієї сторони|Опирання з двох сторін';
type_of_construction_wall['Самонесуча стіна'] = 'Самонесуча';
type_of_construction_wall['Перегородка'] = 'Перегородка';

var width_of_wall = Object();

width_of_wall['Опирання з однієї сторони'] = '250|380|510|640|770|900';
width_of_wall['Опирання з двох сторін'] = '380|510|640|770|900';
width_of_wall['Самонесуча'] = '250|380|510|640|770|900';
width_of_wall['Перегородка'] = '120|250';

function set_type_of_wall()
{
	for (type_of_wall in type_of_construction_wall)
		document.write('<option value="' + type_of_wall + '">' + type_of_wall + '</option>');
}

function set_type_of_construction_wall(type_of_wall_sel, type_of_construction_wall_sel, width_of_wall_sel)
{
	var type_of_construction_wall_array;
	type_of_construction_wall_sel.length = 0;
	width_of_wall_sel.length = 0;
	var type_of_wall = type_of_wall_sel.options[type_of_wall_sel.selectedIndex].text;
	if (type_of_construction_wall[type_of_wall])
	{
		type_of_construction_wall_sel.disabled = false;
		width_of_wall_sel.disabled = true;
//		type_of_construction_wall_sel.options[0] = new Option('---','');
		type_of_construction_wall_array = type_of_construction_wall[type_of_wall].split('|');
		for (var i = 0; i < type_of_construction_wall_array.length; i++)
			type_of_construction_wall_sel.options[i] = new Option(type_of_construction_wall_array[i], type_of_construction_wall_array[i]);
	}
	else type_of_construction_wall_sel.disabled = true;
}

function set_width_of_wall(type_of_construction_wall_sel, width_of_wall_sel)
{
	var width_of_wall_array;
	width_of_wall_sel.length = 0;
	var type_of_construction_wall = type_of_construction_wall_sel.options[type_of_construction_wall_sel.selectedIndex].text;
	if (width_of_wall[type_of_construction_wall])
	{
		width_of_wall_sel.disabled = false;
//		width_of_wall_sel.options[0] = new Option('---','');
		width_of_wall_array = width_of_wall[type_of_construction_wall].split('|');
		for (var i = 0; i < width_of_wall_array.length; i++)
			width_of_wall_sel.options[i] = new Option(width_of_wall_array[i],width_of_wall_array[i]);
	}
	else width_of_wall_sel.disabled = true;
}

function start(type_of_wall_sel, type_of_construction_wall_sel, width_of_wall_sel)
{
    set_type_of_construction_wall(type_of_wall_sel, type_of_construction_wall_sel, width_of_wall_sel);
    set_width_of_wall(type_of_construction_wall_sel, width_of_wall_sel);
}