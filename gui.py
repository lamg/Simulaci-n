import pygtk
pygtk.require('2.0')
import gtk
import stats
import math

class GUI:
	def __init__(self):
		self.st = stats.stats()
			
		self.win = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.win.connect('destroy', self.destroy)
		self.win.set_title('Simulacion')
		self.win.set_default_size(400,300)
		
		self.sel = gtk.combo_box_new_text()
		self.sel.connect('changed', self.changed)
		self.sel.append_text('Prueba de la media')
		self.sel.append_text('Prueba de la varianza')
		self.sel.append_text('Prueba de la forma')
		self.sel.append_text('Prueba de la independencia')
		self.sel.append_text('Todas')
		
		self.cant = gtk.SpinButton()
		self.cant.set_range(5,30)
		self.cant.set_increments(1,1)
		
		self.alfa = gtk.SpinButton(digits=2)
		self.alfa.set_range(0,1)
		self.alfa.set_increments(0.1,0.1)
		self.alfa.set_value(0.1)
		
		self.lst = gtk.ListStore(str)
		self.col = gtk.TreeViewColumn('Numeros')
		self.cell = gtk.CellRendererText()
		self.col.pack_start(self.cell,True)
		self.col.add_attribute(self.cell, 'text', 0)
		self.lstV = gtk.TreeView(self.lst)
		self.lstV.append_column(self.col)
		
		self.box = gtk.VBox()
		self.sup = gtk.HBox()
		self.sup.pack_start(self.sel)
		self.sup.pack_start(self.cant)
		self.sup.pack_start(self.alfa)
		self.box.pack_start(self.sup,expand=False,fill=False)
		self.box.pack_start(self.lstV)
		
		self.win.add(self.box)
		self.win.show_all()
		
	def main(self):
		gtk.main()
	
	def destroy(self, w):
		gtk.main_quit()
	
	def add(self,val):
		iter = self.lst.append()
		self.lst.set(iter,0,val)		
	
	def media(self, cant_num, alpha):
		r = []
		return r
	
	def varianza(self, cant_num, alpha):
		r = []
		return r
	
	def forma(self, cant_num, alpha):
		r = []
		return r
	
	def independencia(self, cant_num, alpha):
		r = []
		return r
	
	def todas(self, cant_num, alpha):
		num_rand_list = []
	        media = False
	        varianza = False
	        forma = False
	        independencia = False
	
	        self.win.set_title("Realizando las Pruebas......")
	
	        while not (media and varianza and independencia and forma):
	            m = 2147483647
	            c = int(math.floor(stats.generate_random() * (m / 2 - 0) + 0))
	            a = int(math.floor(stats.generate_random() * (m / 2 - 0) + 0))
	            seed = int(math.floor(stats.generate_random() * (m / 2 - 0) + 0))
	            num_rand_list = self.st.random_num_congr(seed, a, c, m, cant_num, True)
	            media = self.st.midTest(num_rand_list, a, alpha)
	            varianza = self.st.varianceTest(num_rand_list, alpha, len(num_rand_list))
	            independencia = self.st.independenceTest(num_rand_list, alpha)
	            forma = self.st.shapeTest(num_rand_list, alpha)
		return num_rand_list
	
	def changed(self, w):
		s = self.sel.get_active_text()
		cn = int(self.cant.get_value())
		a = self.alfa.get_value()
		r = []
		self.lst.clear()
		if s == 'Prueba de la media':
			r = self.media(cn,a)
		elif s == 'Prueba de la varianza':
			r = self.varianza(cn,a)
		elif s == 'Prueba de la forma':
			r = self.forma(cn,a)
		elif s == 'Prueba de la independencia':
			r = self.independencia(cn,a)
		elif s == 'Todas':
			r = self.todas(cn,a)
		else:
			s = 'ninguna seleccionada'
		for i in r:
			self.add(str(i))

if __name__ == '__main__':
	g = GUI()
	g.main()
