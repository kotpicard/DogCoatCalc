from wx.lib.newevent import NewEvent as NewEvt

#NAV
NavigationEvent, EVT_NAVIGATION = NewEvt()
SelectDogEvent, EVT_SELECT_DOG = NewEvt()
AddDogEvent, EVT_ADD_DOG = NewEvt()
NavDataPass, EVT_NAV_DATA_PASS = NewEvt()
OpenDogPageEvent, EVT_OPEN_DOG_PAGE = NewEvt()
PassDataForDogPageEvent, EVT_PASS_DATA_DOG_PAGE = NewEvt()
OpenGenotypeViewEvent, EVT_VIEW_GENOTYPE = NewEvt()
PassDataForViewGenotype, EVT_VIEWGEN_DATAPASS = NewEvt()
PassFormattedGenotype, EVT_FORMATTEDGEN_DATAPASS = NewEvt()
EditLocusEvent, EVT_EDIT_LOCUS = NewEvt()
OpenEditLocusEvent, EVT_OPEN_EDIT_LOCUS = NewEvt()
PassGenotypeDataEvent, EVT_PASS_GENOTYPE = NewEvt()
PassEditLocusDataEvent, EVT_PASS_EDIT_LOCUS_DATA = NewEvt()
OpenMainMenu, EVT_MAIN_MENU = NewEvt()

#SAVE/LOAD
SaveEvent, EVT_SAVE = NewEvt()
LoadEvent, EVT_LOAD = NewEvt()
LoadDogFromDataEvent, EVT_LOAD_DOG_FROM_DATA = NewEvt()
PassDogToDataLayerEvent, EVT_PASS_DOG = NewEvt()
PassDogDataEvent, EVT_PASS_DOG_DATA = NewEvt()
DisplayAllDogsEvent, EVT_DISPLAY_ALL_DOGS = NewEvt()
RequestDogByID, EVT_REQUEST_DOG_BY_ID = NewEvt()
RequestGenotypeByID, EVT_REQUEST_GENOTYPE_BY_ID = NewEvt()

#DOG EVENTS
DogIncorrectGenotypeEvent, EVT_INCORRECT_GENOTYPE = NewEvt()
DogGenotypeChangedEvent, EVT_GENOTYPE_CHANGED = NewEvt()
