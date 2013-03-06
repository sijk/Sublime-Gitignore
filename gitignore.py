import sublime, sublime_plugin
import os


class rungiboCommand(sublime_plugin.WindowCommand):

	path = os.path.join(os.path.abspath(os.path.dirname(__file__)),
	                    'boilerplates')

	def run(self):
		self.list = [os.path.splitext(f)[0] for f in os.listdir(self.path)]
		self.chosen = []
		self.window.show_quick_panel(self.list, self.select)

	def select(self, index):
		if index < 0: return

		if index == 0 and self.list[0] == 'Done':
			self.write_file()
			return

		self.chosen.append(self.list.pop(index))

		if self.list[0] != 'Done':
			self.list = ['Done'] + self.list

		self.window.show_quick_panel(self.list, self.select)

	def write_file(self):
		final = ''

		for boilerplate in self.chosen:
			path = os.path.join(self.path, boilerplate + '.gitignore')
			contents = open(path).read()
			final += '### %s ###\n\n%s\n\n' % (boilerplate, contents)

		view = sublime.active_window().new_file()
		edit = view.begin_edit()
		view.insert(edit, 0, final)
		view.set_name('.gitignore')
		view.end_edit(edit)
