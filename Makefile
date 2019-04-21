
# Makefile generated automatically by /home/frederic/utils/scripts/mkcxx.pl '-f' '-l' '-lLundPlane'
# run 'make make' to update it if you add new files

CXX = g++  # for macs - otherwise get c++ = clang
CXXFLAGS = -Wall -g -O2 -std=c++11

FJCONFIG = fastjet-config
INCLUDE += `$(FJCONFIG) --cxxflags`
LIBRARIES  += `$(FJCONFIG) --libs --plugins`
INCLUDE += $(LCLINCLUDE)

COMMONSRC = 
F77SRC = 
COMMONOBJ = 

PROGSRC = example.cc example_secondary.cc
PROGOBJ = example.o example_secondary.o

INCLUDE += 
LIBRARIES += -lLundPlane


all:  example example_secondary 


example: example.o  $(COMMONOBJ)
	$(CXX) $(LDFLAGS) -o $@ $@.o $(COMMONOBJ) $(LIBRARIES)

example_secondary: example_secondary.o  $(COMMONOBJ)
	$(CXX) $(LDFLAGS) -o $@ $@.o $(COMMONOBJ) $(LIBRARIES)


make:
	/home/frederic/utils/scripts/mkcxx.pl '-f' '-l' '-lLundPlane'

clean:
	rm -vf $(COMMONOBJ) $(PROGOBJ)

realclean: clean
	rm -vf  example example_secondary 

.cc.o:         $<
	$(CXX) $(CXXFLAGS) $(INCLUDE) -c $< -o $@
.cpp.o:         $<
	$(CXX) $(CXXFLAGS) $(INCLUDE) -c $< -o $@
.C.o:         $<
	$(CXX) $(CXXFLAGS) $(INCLUDE) -c $< -o $@
.f.o:         $<
	$(F77) $(FFLAGS) -c $< -o $@


depend:
	makedepend  $(LCLINCLUDE) -Y --   -- $(COMMONSRC) $(PROGSRC)
# DO NOT DELETE
