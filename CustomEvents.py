from wx.lib.newevent import NewEvent as NewEvt

#NAV
NavigationEvent, EVT_NAVIGATION = NewEvt()
SelectDogEvent, EVT_SELECT_DOG = NewEvt()
AddDogEvent, EVT_ADD_DOG = NewEvt()
NavDataPass, EVT_NAV_DATA_PASS = NewEvt()
OpenDogPageEvent, EVT_OPEN_DOG_PAGE = NewEvt()
PassDataForDogPageEvent, EVT_PASS_DATA_DOG_PAGE = NewEvt()

#SAVE/LOAD
SaveEvent, EVT_SAVE = NewEvt()
LoadEvent, EVT_LOAD = NewEvt()
LoadDogFromDataEvent, EVT_LOAD_DOG_FROM_DATA = NewEvt()
PassDogToDataLayerEvent, EVT_PASS_DOG = NewEvt()
PassDogDataEvent, EVT_PASS_DOG_DATA = NewEvt()
DisplayAllDogsEvent, EVT_DISPLAY_ALL_DOGS = NewEvt()
RequestDogByID, EVT_REQUEST_DOG_BY_ID = NewEvt()

#DOG EVENTS
DogIncorrectGenotypeEvent, EVT_INCORRECT_GENOTYPE = NewEvt()
