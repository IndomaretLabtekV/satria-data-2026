Received24July2025,accepted24August2025,dateofpublication28August2025,dateofcurrentversion5September2025.
DigitalObjectIdentifier10.1109/ACCESS.2025.3603903
A Review of Computer Vision for
Industrial-Grade Waste Classification
PELLETHIELMANN 1,YUZHOU 1,BRUNOMIRBACH 1,DIDIERSTRICKER 1,2,
ANDJASONRAMBACH 1
1AugmentedVisionDepartment,GermanResearchCenterforArtificialIntelligence(DFKIGmbH),67663Kaiserslautern,Germany
2RPTUKaiserslautern,67663Kaiserslautern,Germany
Correspondingauthor:PelleThielmann(Pelle.Thielmann@dfki.de)
ThisworkwassupportedinpartbytheGermanMinistryofEducationandResearch(BMBF)underGrant033R390(ReVise_UP).
ABSTRACT Theautomationofmunicipalsolidwastesortingisarapidlyadvancingfield,drivenbytheneed
to improve efficiency, accuracy, and recycling outcomes in material recovery facilities. A key component
of this automation is accurate waste classification, where computer vision holds great potential, but most
prior work has been limited to controlled and simplified laboratory setups or in-the-wild scenarios. The
recently published industrial-grade waste datasets, recorded in real-world sorting facilities showing waste
streamsonconveyorbeltswithhighlevelofclutterandocclusion,presentaseverechallengeforstate-of-
the-artcomputervisionmodels.Despitetheirsignificance,thesedatasetshavenotyetbeencomprehensively
reviewed.Thispaperaddressesthatgapbysystematicallyanalyzingandcomparingexistingindustrial-grade
wastedatasets.Wefurthersummarizewell-reportedmodelperformancesandinvestigatemodelarchitectures
and methods evaluated on the presented datasets to support future model development. We identify both
dataset-specificandgeneralchallengesinthisdomainandconcludebyoutliningfutureresearchdirections
toadvanceCV-basedwastesortinginindustrialenvironments.
INDEX TERMS Waste classification, waste sorting, computer vision, object detection, semantic
segmentation,deeplearning,materialrecovery.
I. INTRODUCTION Whereassomefacilitiesstillrelyonhuman-basedmanual
Municipal solid waste (MSW) generation has reached a sorting, process automation is increasingly adopted to
concerning amount, with 2.1 billion tonnes per year world- improve sorting efficiency and accuracy. The automated
widereportedin2020.Accordingtorecentstatistics,MSW waste sorting process can be classified into direct and
production will reach 2.6 billion tonnes per year by 2030. indirectsorting.Directsortingutilizesmaterialpropertieslike
Aportionofaround60%ofthemunicipalwastegeneratedis magnetismanddensity,combinedwithmechanicalprocesses
managedthroughcontrolledprocessessuchaslandfill,waste- for separation, while indirect sorting employs sensors to
to-energy, or recycling. Consequently, approximately 40% detectandsortrecyclables[2].
of municipal waste remains unorganized and uncontrolled, Amongthesesensorsintheindirectsorting,opticalsensors
leading to disposal practices such as open dumping and playakeyroleinthematerialclassificationofwastestreams.
burning [1]. Even among the managed waste, only 30% is Near-infrared (NIR) technology is widely used and highly
recycledorundergoesmaterialrecovery.Thishighlightsthe effective, particularly for pixel-level plastic identification
challengesthatmaterialrecoveryfacilities(MRFs)encounter based on chemical composition. Its ability to distinguish
insortingcollectedmunicipalwaste,emphasizingtheneedto differentpolymersmakesitthedominantmethodforplastic
enhancesortingprocessesandimproverecyclingoutcomes. wastesorting[3].
However, NIR sensors have certain constraints, includ-
The associate editor coordinating the review of this manuscript and ing high costs, relatively low resolution, and sensitivity
approvingitforpublicationwasTurgayCelik . to contaminants like dirt and moisture, which affect the
2025TheAuthors.ThisworkislicensedunderaCreativeCommonsAttribution-NonCommercial-NoDerivatives4.0License.
151934 Formoreinformation,seehttps://creativecommons.org/licenses/by-nc-nd/4.0/ VOLUME13,2025

P.Thielmannetal.:ReviewofComputerVisionforIndustrial-GradeWasteClassification
performance.Additionally,duetotheirpixel-basedapproach, variationsinconsumerbehaviorinfluencethecompositionof
NIR systems struggle with object-/particle-level identifica- waste,asdoshiftsinpackagingdesignovertimeandacross
tion, which is for example crucial for detecting hazardous different markets. These factors create significant domain
objects, preventing machine blockages, and distinguish- shifts,makingwasteclassificationevenmorechallenging.
ing between food and nonfood packaging in recycling Inthispaper,wegiveanin-depthreviewofindustrial-grade
streams[3]. wasteclassificationfromtheperspectiveofCV.Inparticular,
RGBsensorscancomplementNIRbyaddressingsomeof wehighlightfourkeycontributions:
theselimitations.Theyarelow-cost,offerhigherresolution,
• ReviewsofWasteClassification:IntheRelatedWork
| and enable       | object-level |              | recognition |               | and classification |             | [4]. |          |     |             |         |     |          |          |
| ---------------- | ------------ | ------------ | ----------- | ------------- | ------------------ | ----------- | ---- | -------- | --- | ----------- | ------- | --- | -------- | -------- |
|                  |              |              |             |               |                    |             |      | Section, | we  | analyze and | compare |     | existing | reviews, |
| This facilitates |              | the seamless |             | incorporation |                    | of advanced |      |          |     |             |         |     |          |          |
identifytheircontributionsandlimitations,andposition
computervision(CV)methods,whichleveragedeeplearning
ourworkinthisfield.
(DL)modelstoenhancewastesortingbyimprovingmaterial
|                |     |           |           |     |              |     |        | • Dataset | Analysis | and | Comparison: |     | We distinguish |     |
| -------------- | --- | --------- | --------- | --- | ------------ | --- | ------ | --------- | -------- | --- | ----------- | --- | -------------- | --- |
| classification | and | detecting | hazardous |     | or misplaced |     | items. |           |          |     |             |     |                |     |
betweenin-the-wildandindustrial-gradewastedatasets,
| Nevertheless,   | applying |              | CV techniques |                  | in  | industrial | waste |           |                |                     |        |                  |        |          |
| --------------- | -------- | ------------ | ------------- | ---------------- | --- | ---------- | ----- | --------- | -------------- | ------------------- | ------ | ---------------- | ------ | -------- |
|                 |          |              |               |                  |     |            |       | providing | a              | detailed comparison |        | of the           | latter | in terms |
| sorting remains |          | challenging, |               | due to demanding |     | visual     | con-  |           |                |                     |        |                  |        |          |
|                 |          |              |               |                  |     |            |       | of their  | classification | tasks,              | unique | characteristics, |        | and      |
ditionsinsortingfacilitiesandtheneedforrealisticdatasets
limitations.
fortrainingandevaluation.
|               |          |            |             |            |                 |                  |        | • Model | Performance | and            | Challenges: |         | We survey  | CV      |
| ------------- | -------- | ---------- | ----------- | ---------- | --------------- | ---------------- | ------ | ------- | ----------- | -------------- | ----------- | ------- | ---------- | ------- |
| To reflect    | these    | challenges |             | in dataset | design          | and              | appli- |         |             |                |             |         |            |         |
|               |          |            |             |            |                 |                  |        | models  | trained     | on these       | datasets,   | curate  | and        | compare |
| cation, we    | use      | the terms  | in-the-wild |            | and             | industrial-grade |        |         |             |                |             |         |            |         |
|               |          |            |             |            |                 |                  |        | their   | reported    | performances   | from        | various | sources,   | and     |
| to categorize | waste    | datasets   |             | used in    | CV. In-the-wild |                  | waste  |         |             |                |             |         |            |         |
|               |          |            |             |            |                 |                  |        | discuss | the         | key challenges | for         | model   | deployment | and     |
| datasets      | refer to | images     | of waste    | captured   | in              | environmental    |        |         |             |                |             |         |            |         |
trainingassociatedwitheachdataset.
oreverydayhuman-centeredsettings–suchasstreets,parks,
|             |               |                   |              |            |           |             |     | • Future  | Directions: | We    | outline | promising | directions |        |
| ----------- | ------------- | ----------------- | ------------ | ---------- | --------- | ----------- | --- | --------- | ----------- | ----- | ------- | --------- | ---------- | ------ |
| and beaches | –             | or in simplified, |              | controlled |           | background  | or  |           |             |       |         |           |            |        |
|             |               |                   |              |            |           |             |     | of future | research,   | based | on      | observed  | gaps and   | latest |
| lab-scale   | environments. |                   | In contrast, |            | we define | industrial- |     |           |             |       |         |           |            |        |
trends.
| grade waste | datasets | as  | those | captured | in  | MRFs or | waste |     |     |     |     |     |     |     |
| ----------- | -------- | --- | ----- | -------- | --- | ------- | ----- | --- | --- | --- | --- | --- | --- | --- |
sortingfacilities,wherewasteisrecordedonconveyorbelts
under realistic operating conditions. These datasets reflect II. RELATEDWORK
thecomplexvisualcharacteristicsofactualsortingenviron- A. PRIORREVIEWSANDSURVEYS
ments: high clutter, overlapping objects, partial occlusion, Theadvancementofwasteclassificationhasbeenthesubject
deformations,contaminationandvaryinglightingconditions. ofnumerousresearcheffortsovertheyears,resultinginvar-
Importantly, the term ‘‘industrial-grade’’ mainly refers to iousreviewstudiesthatexplorethisfieldfromdifferentper-
the data acquisition context and visual complexity of the spectives and with different scopes. Whereas some reviews
dataset, rather than the specific type of waste it contains. focus on automation in waste sorting, others emphasize AI-
We consider the type of waste as a secondary aspect in this driven methods, sensor technologies, or dataset availability.
categorization and limit our scope to industrial-grade waste In this section, we provide an overview of recent review
datasetscontaininghouseholdormunicipalsolidwaste. papers, highlighting their contributions and outlining their
ZeroWaste [5], the first industrial-grade waste dataset limitationsbeforepositioningourstudywithinthisresearch
landscape.
| introduced | in 2022, | showed |     | that common |     | CV models | fail |     |     |     |     |     |     |     |
| ---------- | -------- | ------ | --- | ----------- | --- | --------- | ---- | --- | --- | --- | --- | --- | --- | --- |
to achieve acceptable performance for waste detection and One of the foundational works in this area is the
segmentation. While in-the-wild waste datasets share visual review by [2], which provides a fundamental overview
characteristics with classic object detection and semantic of the structure, techniques and systems of an automated
segmentation datasets, industrial-grade waste datasets stand sorting process for MSW. The study examines applicable
|     |     |     |     |     |     |     |     | technologies | for | different recyclable |     | materials | in MSW | and |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | -------------------- | --- | --------- | ------ | --- |
insharpcontrastduetotheirhighlevelofclutter,occlusion,
anddeformation.Thisfundamentalbiascreatesasubstantial highlightsthewidespreadadoptionandcriticalroleofoptical
domain gap, making it difficult for pretrained models – sensorsinmodernsortingsystems.Notably,theauthorsalso
trained on such human-centered datasets – to extract robust emphasizeearlyontheimportanceofsensoranddatafusion
and meaningful features when applied to waste streams toimprovesortingefficiencyandreliability–pointingtoward
on conveyor belts. Another concern is the general data thefutureneedformoreintegrated,intelligentsystems.Atthe
scarcity for waste datasets recorded in sorting facilities time, however, CV technologies remained in their infancy,
with only a few industrial-grade waste datasets publicly andtheirpotentialroleinautomatedsortinghadnotyetbeen
available.Thiscanbetracedbacktotheextensiveannotation fullyexplored.
overhead for these datasets limiting also the overall amount Thereviewin[11]coveredAIapplicationsacrossvarious
of annotated images. In addition, waste is highly domain solidwastemanagement(SWM)fields,includingforecasting
specific. Waste sorting and collection systems vary not of waste characteristics, waste bin level detection, process
only between countries but also within regions of the same parametersandprocessoutputprediction,vehicleroutingand
country,leadingtodiversewastestreams.Moreover,seasonal SWMplanning.Theauthorsfoundthatkeychallenges–such
| VOLUME13,2025 |     |     |     |     |     |     |     |     |     |     |     |     |     | 151935 |
| ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |

P.Thielmannetal.:ReviewofComputerVisionforIndustrial-GradeWasteClassification
FIGURE1. Wastedatasetsgroupedinto‘‘in-the-wild’’and‘‘industrial-grade’’accordingtovisualfeaturesandplaceofrecording.Left:Sample
imagesofin-the-wildwastedatasetsTrashNet[6],TACO[7],andReSORT-IT[8].Right:Sampleimagesofindustrial-gradewastedatasets
WaRP[9],SpectralWaste[10]andZeroWaste[5].
as insufficient data, lack of research continuity, the closed- convolutional neural networks (CNNs), and highlights a
box nature of AI models, limited tailored solutions, and shift from pixel-level analysis toward broader applications
slowindustryadoption–hinderwidespreadimplementation, such as material flow monitoring and process control.
highlightingthenecessityformultidisciplinarycollaboration Significant research gaps remain at the flow and process
and industry integration. Similar findings were reported levels,asmoststudiesarelimitedtolabscale.Furthermore,
in another review [12] that focused specifically on AI the authors highlight the promising potential of low-cost
applications in SWM within Australia. In addition, they RGBsensorscombinedwithadvancedalgorithmstoenable
provide concrete policy and industry recommendations, affordable, scalable material classification for real-world
emphasizing the need for improved digital infrastructure, sortingapplications.
regulatory frameworks, AI transparency, community educa- Theworksin[4]and[13]bothreviewtherapiddevelop-
tion,andnationalcollaboration,whilealsoplacingastronger mentofCVinwastesortingandwasteidentification,likewise
focus on sustainability through waste reduction, enhanced emphasizing the shift from traditional machine learning to
recycling,andwaste-to-energystrategies.Both[11]and[12] deep learning approaches due to their superior robustness
highlight the significant potential of AI in enhancing SWM andend-to-endlearningcapabilities.Theyanalyzecommon
by offering more efficient, data-driven solutions where modelarchitectures,taskobjectives(classification,detection,
traditional methods fall short. However, their focus remains segmentation),andstresstheimportanceofpubliclyavailable
on a broad range of classic AI algorithms such as support datasets, still scarce and often focused on simplified lab
vectormachines(SVMs),decisiontrees,andartificialneural environments, highlighting the need for more real-world
networks (ANNs), with limited attention given to state-of- applicable resources. Additionally, [13] highlight the rising
the-art CV-based methods. As a result, the transformative attentiontomunicipalsolidwasteandthefutureimportance
potential of DL approaches – particularly in improving of object detection and segmentation in intelligent waste
wasteclassification,characterization,andsortingprocedures identification and recycling. Both reviews compare model
–remainsunderexploredinthesereviews. performances primarily on the TrashNet [6] dataset, which,
The authors in [3] provide a comprehensive review of while useful for evaluating algorithmic potential, is too
sensor-based material flow characterization methods using simplistic to reflect real-world industrial conditions. This
opticalsensorsandmachinelearningalgorithmsinthecon- exposesabroaderlimitation–theabsenceofastandardized,
textofdrymechanicalrecyclingofnonhazardouswaste.The benchmarkdatasetsuitableforindustrial-gradewasteclassi-
reviewrevealsagrowingfocusonDLapproaches,especially fication.
151936 VOLUME13,2025

P.Thielmannetal.:ReviewofComputerVisionforIndustrial-GradeWasteClassification
In line with this, [14] underscore the lack of open, simplified context, which we refer to as in-the-wild waste
high-quality waste datasets particularly those reflecting real datasets,andthosecollectedfromwastesortingfacilitieswith
sorting conditions such as material clusters on conveyor clutteredwastestreamsonconveyorbelts,whichwelabelas
belts.Theauthorsidentifyacriticalgapinpubliclyavailable industrial-grade waste datasets. The contrast between these
datasets specifically targeting post-consumer plastic waste twocategoriesisillustratedinFig.1.
with fractions like polyethylene terephthalate (PET), high- We begin by providing an overview of in-the-wild waste
density polyethylene (HDPE), or low-density polyethylene datasets, briefly outlining the contexts and scenarios they
(LDPE)–especiallywithinthecontextofindustrialfacilities aim to represent. In TrashNet [6], one of the first waste
such as German plastic sorting plants. Furthermore, the datasets,recyclablewasteobjectswerecapturedonasimple
review investigates the availability and limitations of RGB whitebackgroundsolelyforimageclassificationtask.Inthe
andNIRdatasetsformachinelearningapplicationsinplastic TACO [7] dataset, waste objects were captured in various
wastesorting,emphasizingtheneedformultisensorydata. environments such as beaches or pavements to enable litter
detection.TACObenefitsfromcrowd-sourceddatacollection
andannotationfromallovertheworld.Itwasoneofthefirst
B. SCOPEANDPOSITIONING
wastedatasetsforobjectsegmentationaddingtheimportant
| Prior reviews |     | and surveys |     | tend to | fall | in one | of the |     |     |     |     |     |     |     |
| ------------- | --- | ----------- | --- | ------- | ---- | ------ | ------ | --- | --- | --- | --- | --- | --- | --- |
localizationofobjectswithintheimage.Verysimilardatasets
| following | categories: |     | broad | surveys | of AI | in solid | waste |     |     |     |     |     |     |     |
| --------- | ----------- | --- | ----- | ------- | ----- | -------- | ----- | --- | --- | --- | --- | --- | --- | --- |
toTACOareOpenLitterMap[16]andDomesticTrash[17],
| management,          |             | analyses | of sensor-based |           | or      | robotic   | sorting |               |          |                  |           |       |            |             |
| -------------------- | ----------- | -------- | --------------- | --------- | ------- | --------- | ------- | ------------- | -------- | ---------------- | --------- | ----- | ---------- | ----------- |
|                      |             |          |                 |           |         |           |         | which also    | leverage | collaborative    |           | data  | gathering. | Another     |
| systems,             | or studies  | focusing |                 | on CV     | methods | trained   | on      |               |          |                  |           |       |            |             |
|                      |             |          |                 |           |         |           |         | waste dataset |          | targeting litter | detection |       | is FloW    | [18] with   |
| simplified,          | in-the-wild |          | waste           | datasets. | Across  | these     | works,  |               |          |                  |           |       |            |             |
|                      |             |          |                 |           |         |           |         | the specific  | domain   | of floating      |           | waste | objects.   | These waste |
| the industrial-grade |             | setting  | defined         | by        | us –    | cluttered | waste   |               |          |                  |           |       |            |             |
datasetsoftenfeaturewasteitemsineverydayenvironments
streamsrecordedonconveyorbeltswithinsortingfacilities–
orsimplifiedbackgrounds.
| remains  | underexplored. |          | Furthermore, |          | a systematic |           | compar- |           |      |          |         |      |      |               |
| -------- | -------------- | -------- | ------------ | -------- | ------------ | --------- | ------- | --------- | ---- | -------- | ------- | ---- | ---- | ------------- |
|          |                |          |              |          |              |           |         | A dataset | that | does not | clearly | fall | into | either of the |
| ison and | in-depth       | analysis | of           | existing | waste        | datasets, | their   |           |      |          |         |      |      |               |
categoriesisReSORT-IT[8].Itwasrecordedinacontrolled
individualcharacteristicsandlimitationsandtheCVandDL
environmentonaconveyorbelt,whereindividualrecyclable
modelstrainedonthesedatasetsisnotexistenttillnow.
objectswerecapturedinisolationagainstablackbackground.
Wenarrowedourscopeandspecificallytargettheemerg-
Thedatasetwasthenexpandedthroughsyntheticaugmenta-
| ing field | of CV-based |     | industrial-grade |     | waste | classification, |     |     |     |     |     |     |     |     |
| --------- | ----------- | --- | ---------------- | --- | ----- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- |
tion–firstwithsingle-objectscenes,thenwithsynthetically
| which has | seen | a sharp | increase | in  | research | output | over |     |     |     |     |     |     |     |
| --------- | ---- | ------- | -------- | --- | -------- | ------ | ---- | --- | --- | --- | --- | --- | --- | --- |
overlappedones.Whiletheconveyorsetupmimicsindustrial
| the past | years. | This growth | has | been | largely | driven | by the |             |     |            |              |     |            |         |
| -------- | ------ | ----------- | --- | ---- | ------- | ------ | ------ | ----------- | --- | ---------- | ------------ | --- | ---------- | ------- |
|          |        |             |     |      |         |        |        | conditions, | the | absence of | real clutter | and | occlusions | sets it |
releaseofpubliclyavailable,industrial-gradewastedatasets,
apartfromtrueindustrial-gradedatasets.
| which provide |            | the foundation |            | for developing |             | CV       | models in |              |         |           |       |          |          |                 |
| ------------- | ---------- | -------------- | ---------- | -------------- | ----------- | -------- | --------- | ------------ | ------- | --------- | ----- | -------- | -------- | --------------- |
|               |            |                |            |                |             |          |           | All datasets |         | mentioned | so    | far are  | publicly | available.      |
| this domain.  | Therefore, |                | we conduct |                | an in-depth | analysis | of        |              |         |           |       |          |          |                 |
|               |            |                |            |                |             |          |           | However,     | several | private   | waste | datasets | exist    | that are either |
bothdatasetsandmodelsfromaCVperspective,focusingon
|     |     |     |     |     |     |     |     | only accessible |     | upon request | or  | remain | completely | closed. |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------- | --- | ------------ | --- | ------ | ---------- | ------- |
howdatasetcharacteristicsinfluencemodelperformanceand
|     |     |     |     |     |     |     |     | [19] created |     | a database | called | WaDaBa | for | categorizing |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | ---------- | ------ | ------ | --- | ------------ |
applicabilityinindustrialsettings.Bydistinguishingbetween
|             |     |                  |     |            |     |     |           | household | plastic | waste | items into | 4 plastic | polymers, | with |
| ----------- | --- | ---------------- | --- | ---------- | --- | --- | --------- | --------- | ------- | ----- | ---------- | --------- | --------- | ---- |
| in-the-wild | and | industrial-grade |     | scenarios, |     | we  | provide a |           |         |       |            |           |           |      |
singleitemsrecordedonblackbackground.Anotherprivate
| structured | comparison |     | of publicly | available |     | datasets | of the |     |     |     |     |     |     |     |
| ---------- | ---------- | --- | ----------- | --------- | --- | -------- | ------ | --- | --- | --- | --- | --- | --- | --- |
dataset[20]focusesoncontaminationdetectionduringwaste
latter.Toourknowledge,thisisthefirstreviewtosystemati-
|     |     |     |     |     |     |     |     | collection | with | cameras | mounted | on  | the garbage | truck. |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | ---- | ------- | ------- | --- | ----------- | ------ |
callycompileandcomparewell-documentedresultsreported
|              |           |     |          |           |         |     |            | In addition, | several | companies |     | and industry |     | stakeholders |
| ------------ | --------- | --- | -------- | --------- | ------- | --- | ---------- | ------------ | ------- | --------- | --- | ------------ | --- | ------------ |
| across these | datasets, |     | enabling | a clearer | picture |     | of current |              |         |           |     |              |     |              |
activeinthefieldofautomatedwastesortinghavedeveloped
modelcapabilities,identifyingkeychallenges,andoutlining
|                 |     |             |       |        |           |     |            | their own      | private | datasets   | to train    | CV  | models        | tailored to |
| --------------- | --- | ----------- | ----- | ------ | --------- | --- | ---------- | -------------- | ------- | ---------- | ----------- | --- | ------------- | ----------- |
| future research |     | directions. | Thus, | our    | objective | is  | to support |                |         |            |             |     |               |             |
|                 |     |             |       |        |           |     |            | their specific |         | use cases. | One example |     | is Recycleye, | which       |
| the development |     | of computer |       | vision | methods   | for | industrial |                |         |            |             |     |               |             |
claimstohavecompiledWasteNet[21],aproprietarydataset
| waste sorting |     | by providing | a   | solid foundation |     | for | building |            |      |           |           |       |        |          |
| ------------- | --- | ------------ | --- | ---------------- | --- | --- | -------- | ---------- | ---- | --------- | --------- | ----- | ------ | -------- |
|               |     |              |     |                  |     |     |          | containing | over | 3 million | annotated | waste | images | captured |
andevaluatinghigh-performingmodelsgroundedinrealistic
inoperationalsortingfacilities.Whiletheseprivatedatasets
| data and             | task | conditions. | We        | see this | as a    | key enabler | for       |                |        |          |                |         |                |       |
| -------------------- | ---- | ----------- | --------- | -------- | ------- | ----------- | --------- | -------------- | ------ | -------- | -------------- | ------- | -------------- | ----- |
|                      |      |             |           |          |         |             |           | offer valuable |        | insights | and real-world |         | applicability, | their |
| further improvements |      | in          | automated | waste    | sorting |             | and other |                |        |          |                |         |                |       |
|                      |      |             |           |          |         |             |           | restricted     | access | limits   | their          | use for | benchmarking   | and   |
applicationswithinthewastemanagementfield.
|     |     |     |     |     |     |     |     | academic | model | development. | As  | such, | our review | focuses |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ----- | ------------ | --- | ----- | ---------- | ------- |
exclusivelyonpublicdatasetsthatcanbeshared,reproduced,
III. DATASETCOMPARISON andcomparedbythebroaderresearchcommunity.
A. IN-THE-WILDVS.INDUSTRIAL-GRADEWASTE Intheremainderofthissection,weturnourfocustopublic
DATASETS
industrial-gradewastedatasets,thatwererecordedinmaterial
Inthissubsection,wedistinguishbetweentwotypesofwaste recovery or sorting facilities and show cluttered waste
datasets: those captured in a more human-centered and/or streams on conveyor belts, including naturally occurring
| VOLUME13,2025 |     |     |     |     |     |     |     |     |     |     |     |     |     | 151937 |
| ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |

P.Thielmannetal.:ReviewofComputerVisionforIndustrial-GradeWasteClassification
TABLE1. Metadataforindustrial-gradewastedatasets.
| occlusions | and | object | deformations. | From | our | perspective, |     |     |     |     |     |     |
| ---------- | --- | ------ | ------------- | ---- | --- | ------------ | --- | --- | --- | --- | --- | --- |
1) RECORDINGDETAILS
the datasets ZeroWaste [5], ZeroWaste-v2 [15], WaRP [9], Therecordingsetupiswelldocumentedbytheauthors.The
and SpectralWaste [10] meet this criteria and are regarded data was captured using a GoPro Hero 7 camera mounted
by us as industrial-grade. Our focus lies on municipal solid 100 cm above the conveyor belt right before the manual
wastedatasets,excludingconstructionanddemolitionwaste sorting. For the subset ZeroWaste-w, an additional camera
orotherwastedomains.
wasmountedafterthemanualsorting,gatheringbefore-and-
The following sections analyze the datasets respectively afterdataforweakly-supervisedlearningmethods.12videos
in terms of general information, recording details, the wererecordedwithatotallengthof95minandaframerate
annotation process, class distribution, and object counts. of 120 fps. Frames were extracted from the videos at
Limitationsarediscussedbrieflyhere,withchallengesfrom intervalsofevery10thand100thframe.Thedensersampling
aCVperspectivecoveredinSectionIV.
resultsinoverlappingframesthatenableobjecttracking.The
frameswererotatedandcroppedtoonlyshowtheconveyor
|     |     |     |     |     |     |     | belt parallel | to the | frame | borders. In | addition, | the optical |
| --- | --- | --- | --- | --- | --- | --- | ------------- | ------ | ----- | ----------- | --------- | ----------- |
B. ZEROWASTE
The first industrial-grade waste dataset is ZeroWaste [5] distortion caused by the camera’s fish-eye effect has been
|         |           |        |     |                |       |           | removed. | Further, | they reduced | the | motion | blur from the |
| ------- | --------- | ------ | --- | -------------- | ----- | --------- | -------- | -------- | ------------ | --- | ------ | ------------- |
| showing | the waste | stream | of  | a high-quality | paper | recycling |          |          |              |     |        |               |
movingconveyorbelt.
conveyor.Thescopeofthedatasetistodetectnonpaperitems
|                  |     |           |           |         |           |              | The ZeroWasteAug |           | subset | includes   | all     | frames from |
| ---------------- | --- | --------- | --------- | ------- | --------- | ------------ | ---------------- | --------- | ------ | ---------- | ------- | ----------- |
| (e.g. cardboard, |     | plastic,  | or metal) | leaving | only      | high-quality |                  |           |        |            |         |             |
|                  |     |           |           |         |           |              | ZeroWaste-f,     | augmented | with   | additional | objects | from the    |
| paper on         | the | conveyor. | Objects   | are     | annotated | in four      |                  |           |        |            |         |             |
material classes cardboard, rigid plastic, metal and soft underrepresented classes metal and rigid plastic, sourced
|                   |        |           |          |             |               |            | from the     | in-the-wild | waste      | dataset TACO | [7].   | To mitigate     |
| ----------------- | ------ | --------- | -------- | ----------- | ------------- | ---------- | ------------ | ----------- | ---------- | ------------ | ------ | --------------- |
| plastic for       | object | detection | and      | semantic    | segmentation. | The        |              |             |            |              |        |                 |
|                   |        |           |          |             |               |            | domain shift | between     | the source | and          | target | domains, visual |
| dataset comprises |        | four      | subsets: | ZeroWaste-f | for           | supervised |              |             |            |              |        |                 |
learning, ZeroWaste-s for unsupervised or self-supervised properties of the cropped TACO objects – specifically
contrast,brightness,andblurriness–wereadjustedtoclosely
| learning, | ZeroWaste-w |     | for weakly-supervised |     | learning, | and |     |     |     |     |     |     |
| --------- | ----------- | --- | --------------------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
ZeroWasteAug, which addresses naturally occurring class align with those of the target frame prior to augmentation.
Additionally,randomresizing,croppingandmirroringwere
| imbalances | through | data | augmentation. |     | An overview | of the |     |     |     |     |     |     |
| ---------- | ------- | ---- | ------------- | --- | ----------- | ------ | --- | --- | --- | --- | --- | --- |
appliedtotheTACOobjectsbeforeaugmentation.
metadataisprovidedinTable1.
| 151938 |     |     |     |     |     |     |     |     |     |     |     | VOLUME13,2025 |
| ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------- |

P.Thielmannetal.:ReviewofComputerVisionforIndustrial-GradeWasteClassification
TABLE2. ObjectsperclassforZeroWaste-fandnumberofaugmented
objectsforZeroWasteAuginblue.
FIGURE2. SampleimagefromZeroWastewithprovidedclasses,
boundingbox,andmaskannotationsrespectively.
2) ANNOTATION
TheclasslabelswerechosentomatchtheMRFguidelinesfor
FIGURE3. NumberofobjectsperimageforZeroWaste-fand
ZeroWasteAug.
theworkerssortingcardboard,metalandplasticintoseparate
bins.Thematerial‘‘plastic’’wassubdividedintoclassessoft
plasticandrigidplastictoaccountforthedifferentgrasping
| strategies | that may be | required | by robotic | systems.     | Objects |               |            |     |                 |          |     |
| ---------- | ----------- | -------- | ---------- | ------------ | ------- | ------------- | ---------- | --- | --------------- | -------- | --- |
|            |             |          |            |              |         | higher object | counts due | to  | the intentional | addition | of  |
| belonging  | to the four | material | classes    | – cardboard, | metal,  |               |            |     |                 |          |     |
augmentedobjects.
soft plastic, and rigid plastic – were manually annotated Inadditiontotheobjectcountdistribution,theobjectsize
| using polygons | in CVAT | [22], | an open-source |     | annotation |     |     |     |     |     |     |
| -------------- | ------- | ----- | -------------- | --- | ---------- | --- | --- | --- | --- | --- | --- |
distributioncanplayasignificantroleinmodelperformance,
tool, providing both bounding box and mask annotations aswewillseeinSectionIV.AsshowninFig.4,aboxplotof
as shown in Fig. 2. Partially occluded objects with visible relative bounding box areas reveals that cardboard and soft
separatepartswereannotatedasindividualinstances,astheir
plasticobjectsaregenerallylarger,withsoftplasticfeaturing
unity cannot be verified. Annotations were reviewed by an the largest and most varied sizes. In contrast, metal objects
| expert to | ensure consistency. |     | The average   | annotation   | time |                    |             |                  |                |            |         |
| --------- | ------------------- | --- | ------------- | ------------ | ---- | ------------------ | ----------- | ---------------- | -------------- | ---------- | ------- |
|           |                     |     |               |              |      | tend to be         | smaller and | more             | compact, while | rigid      | plastic |
| per frame | was recorded        | at  | 12.5 minutes, | highlighting | the  |                    |             |                  |                |            |         |
|           |                     |     |               |              |      | shows intermediate | size        | characteristics. | These          | variations | in      |
significantannotationeffortrequiredforaccuratelylabeling object size can complicate detection tasks, particularly for
wasteobjectsonconveyorbelts.
smaller,lessvisuallyprominentclasseslikemetal.
|     |     |     |     |     |     | It is important | to note, | however, | that | the number | of  |
| --- | --- | --- | --- | --- | --- | --------------- | -------- | -------- | ---- | ---------- | --- |
annotatedobjectsperimageonlypartiallyreflectstheoverall
3) DATASETDETAILS
|               |                |          |              |                |        | scene complexity. | In real-world        |     | conveyor       | belt scenarios | –    |
| ------------- | -------------- | -------- | ------------ | -------------- | ------ | ----------------- | -------------------- | --- | -------------- | -------------- | ---- |
| The ZeroWaste | dataset        | exhibits | a pronounced | natural        | class  |                   |                      |     |                |                |      |
|               |                |          |              |                |        | as is typical     | for industrial-grade |     | waste datasets | –              | many |
| imbalance,    | with cardboard |          | being the    | most prevalent | class, |                   |                      |     |                |                |      |
framescontainadditionalbackgroundmaterialwhichisofno
| followed | by soft plastic. | In  | contrast, | rigid plastic | appears |     |     |     |     |     |     |
| -------- | ---------------- | --- | --------- | ------------- | ------- | --- | --- | --- | --- | --- | --- |
interestornonclassifiable,andthereforenotannotated.These
| less frequently, | while | metal | is considered | rare, | accounting |     |     |     |     |     |     |
| ---------------- | ----- | ----- | ------------- | ----- | ---------- | --- | --- | --- | --- | --- | --- |
for only approximately 1.5% of the total annotated objects. elementscontributetosignificantvisualclutterandincrease
thechallengeofreliableobjectrecognition.
| To overcome | this class | imbalance, | metal | and | rigid plastic |     |     |     |     |     |     |
| ----------- | ---------- | ---------- | ----- | --- | ------------- | --- | --- | --- | --- | --- | --- |
objectswereaugmentedinZeroWasteAugtomatchroughly
with the number of soft plastic objects. All numbers can be 4) LIMITATIONS
foundinTable2. Thesuboptimalcameraposition–notdirectlycenteredover
Beyond class distribution, the dataset also presents a theconveyor–alongwithmotionblurandstrongdistortion,
diverse range of object counts per image. As illustrated requireheavypre-processing,leadingtoinformationlossand
in Fig. 3, object counts range from 0 to 19, with the reducedimagequality.
majority of images containing between 3 and 7 annotated Brown paper, which is labeled as background, appears
objects. Notably, over 500 images contain 10 or more visually similar to cardboard. The distinction between the
objects, underscoring the high complexity of many scenes. twomainlydependsonphysicalpropertieslikethicknessand
Some frames without annotations also reflect real-world rigidity, which are difficult to assess from top-view images
conditions where no relevant waste objects are present. alone.Similarly,thedistinctionbetweensoftandrigidplastic
In ZeroWasteAug, this distribution shifts further toward can be ambiguous, with unclear classification boundaries.
| VOLUME13,2025 |     |     |     |     |     |     |     |     |     |     | 151939 |
| ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |

P.Thielmannetal.:ReviewofComputerVisionforIndustrial-GradeWasteClassification
These challenges are also reflected in reduced annotator
agreementforthesematerialclasses[5].
In analyzing the provided dataset, a discrepancy was
observedbetweenthenumberofinstancesperclassasstated
by the authors in the paper and the actual counts derived
from the available annotation files listed in Table 2. While
the authors reported specific class frequencies, our analysis
of the annotation files revealed different class distributions,
and thus, the reported values in this study reflect the actual
countsobtainedfromthepublisheddatasetannotations.
5) ZEROWASTE-V2
In the Visual Domain Adaptation (VisDA) 2022 Chal-
lenge [15] ZeroWaste-v2 was introduced. It was recorded
in a different sorting facility and during a different season
thanZeroWaste,butwiththesamewastestreamandsorting
guidelines. This setting was designed to reflect the natural
variability in input waste streams caused by factors such
as geographical location, facility-specific processing equip-
ment, and seasonal differences. These factors significantly
influence the composition and visual appearance of waste,
resulting in a natural domain shift that challenges the
generalizationcapabilitiesofCVmodels.Unlessadditional,
often costly, data collection and annotation are conducted,
such domain shifts can severely limit the performance and
deploymentofmodelstonewfacilitiesordifferentseasons.
Thecorechallengeistoapplydomainadaptationtechniques
that allow models trained on the original ZeroWaste dataset
FIGURE4. Objectsizedistributionacrossclasses.a),b):Relative
(source domain) to effectively adapt to the ZeroWaste-v2 boundingboxareadistributionofobjectsacrosstheclassesofa)
dataset(targetdomain).Tosupportthis,theauthorsprovide ZeroWaste-fandb)WaRP-D.c):Relativemaskareadistributionof
instancesacrosstheclassesofSpectralWaste.SeetheAnnotationsection
asmalllabeleddatasetforvalidationandtesting,alongwith
ofSpectralWastefordetailsoninstancedefinitionforthisdataset.
unlabeleddatafortraininginthetargetdomain.Additionally,
they introduced the SynthWaste dataset – a procedurally
generatedsyntheticwastedataset–aimedatimprovingmodel
generalizationandrobustnesstodomainshifts.Moredetails
ondatasetsizesandsplitscanbefoundinTable1.
The real-world ZeroWaste-v2 dataset was recorded and
processed in the same way as ZeroWaste. The SynthWaste
datasetwasgeneratedprocedurallyusingtheUnityDevelop-
mentPlatform,featuringvariousrecyclableobjectsrandomly
placedonaconveyorbelt.Keysimulationparameters–such
as lighting (type, intensity, direction, color), camera angle
and position, level of clutter, and object class distribution
– were randomized during generation. To further address
FIGURE5. SampleimageoftheSynthWastesubsetofZeroWaste-v2.
style differences between synthetic and real data, a texture-
randomized version of the dataset was created, called
SynthWasteAug. Using Domain Aware Universal Style Although the authors provided a large synthetic dataset,
Transfer (DAUST) [23], each object instance is augmented none of the best performing methods from this challenge
withtexturessampledfromtheFlickrMaterialDatabase[24] incorporateditintotheirtrainingpipeline–indicatingthatthe
basedonmaterialtype. SynthWastesubsetmaylacksufficientrealismtoeffectively
Objects were classified following the ZeroWaste guide- supportdomainadaptation(seeFig.5).
lines.Astheannotationsareprovidedsolelyinamaskimage
format,theydonotdistinguishbetweenindividualinstances C. WARP
amongeachclass,limitingthetasktosemanticsegmentation Wastesortingisacomplexprocessthattakesintoaccountnot
only. only the material but also other aspects of waste items, e.g.
151940 VOLUME13,2025

P.Thielmannetal.:ReviewofComputerVisionforIndustrial-GradeWasteClassification
TABLE3. ObjectcountspercategoryandsubcategoryforWaRP-DinTrain
andTestsplits.
FIGURE6. SampleimageofWaRPwiththeprovidedboundingboxand
classannotations.
packagingproductsaresortedbyusagepurpose,plasticcolor
and object type. In the Waste Recycling Plant (WaRP) [9]
dataset, these aspects are considered, resulting in five main
categories and 28 subcategories of recyclable waste objects
tobeclassifiedanddetected.Thedatasetcontains3subsets:
WaRP-Dforobjectdetection,WaRP-Cforclassification,and
WaRP-S for validation of weakly-supervised segmentation
methods. The corresponding metadata can be found in
Table1.
1) RECORDINGDETAILS
The authors do not provide any details about the camera
systemusedforrecording.TheWaRP-CandWaRP-Ssubsets
consistofcroppedimageareasfromWaRP-D,eachlabeled
forclassificationandfeaturingvaryingimagesizes.However,
thecroppingprocessisnotfurtherdescribedbytheauthors,
althoughitcanbeassumedthattheannotatedboundingboxes
wereusedforcropping.
2) ANNOTATION
Theobjectclasseswereselectedtoenabletheidentification
of recyclable items on the conveyor belt of the recycling
facility, with a primary focus on packaging commonly
used for household liquids and beverages. This led to the
definitionoffivemainclasses:bottle,cardboard,detergents,
canisters, and cans. For the classes bottle and detergents,
subcategoriesfurtherdistinguishtheobjectsbasedoncolor,
while subcategories for cardboard reflect usage purpose –
bothofwhichareimportantfactorsfortherecyclingprocess.
Thebottleclasscomprisestwodistinctmaterialtypes:plastic
and glass. Subclasses prefixed with bottle- refer to plastic
bottles, while those under the glass- prefix correspond
to glass bottles. Additionally, the bottle class includes
subclasses with the suffix -full, indicating bottles filled
with air. This distinction is made to account for variations
in grasping and manipulation technologies required during
automatedsorting.Itshouldalsobenotedthatthecardboard FIGURE7. SampleimagecropsofWaRPcategoriesandsubcategories.
class in this context refers specifically to beverage cartons,
suchasthoseusedformilk.Theobjectboundingboxeswere
manuallyannotatedwithasampleimageoftheprovideddata and subcategories with sample image crops is presented in
andannotationsshowninFig.6.Anoverviewofallclasses Fig.7.
VOLUME13,2025 151941

P.Thielmannetal.:ReviewofComputerVisionforIndustrial-GradeWasteClassification
|     |     |     |     |     |     |     | localization | accuracy, | introduce |     | ambiguity | during | training, |     |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --------- | --------- | --- | --------- | ------ | --------- | --- |
andpotentiallylowerIoUscoresduringevaluation.
|     |     |     |     |     |     |     | It is | important | to note | that | the number | of  | objects | per |
| --- | --- | --- | --- | --- | --- | --- | ----- | --------- | ------- | ---- | ---------- | --- | ------- | --- |
classpresentedinTable3differsfromthenumbersreported
|     |     |     |     |     |     |     | in the | WaRP | paper. As | for | ZeroWaste, | the | dataset | was |
| --- | --- | --- | --- | --- | --- | --- | ------ | ---- | --------- | --- | ---------- | --- | ------- | --- |
analyzedbasedontheprovideddataandannotationfiles,with
|     |     |     |     |     |     |     | the reported | class | distributions |     | reflecting | the | actual | counts |
| --- | --- | --- | --- | --- | --- | --- | ------------ | ----- | ------------- | --- | ---------- | --- | ------ | ------ |
obtainedfromtheseannotations.
|     |     |     |     |     |     |     | D. SPECTRALWASTE |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- |
FIGURE8. NumberofobjectsperimageforWaRP-D. Apart from recyclable objects, waste streams in sorting
|     |     |     |     |     |     |     | facilities | also       | contain | objects | that can      | cause | operational |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ---------- | ------- | ------- | ------------- | ----- | ----------- | --- |
|     |     |     |     |     |     |     | problems   | or require | manual  |         | intervention. | The   | authors     | of  |
SpectralWaste[10]createdadatasettosegmentwasteobjects
3) DATASETDETAILS
thatimpactthesortingprocess.Furthermore,SpectralWaste
| The WaRP | dataset | presents | a natural | class | imbalance | that |     |     |     |     |     |     |     |     |
| -------- | ------- | -------- | --------- | ----- | --------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
isthefirstmultimodalindustrial-gradewastedatasetprovid-
| reflects | the real-world | frequency |     | of various | waste | objects |     |     |     |     |     |     |     |     |
| -------- | -------------- | --------- | --- | ---------- | ----- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
ingRGBandhyperspectralimaging(HSI)datafromawaste
withintherecyclingstream.Thebottleclassisbyfarthemost
streamonaconveyorbelt.Subsetsandfurtherinformationon
prevalent,accountingforover70%ofallannotatedobjects.
thedatasetarepresentedinTable1.
Incontrast,thecardboard,detergent,andcanclassesappear
| with moderate |     | frequency, | while the | canister | class | is rare, |     |     |     |     |     |     |     |     |
| ------------- | --- | ---------- | --------- | -------- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
comprising less than 2% of labeled instances. The number 1) RECORDINGDETAILS
of instances per category and subcategory for the WaRP-D For data acquisition, the authors used two synchronized
subsetcanbefoundinTable3. line-scan cameras mounted side-by-side over a conveyor
A closer inspection of the subcategory distribution of the belt. The RGB camera (Teledyne DALSA Line) recorded
bottle class reveals a clear internal imbalance: transparent data is stored at 1200 × 1184 resolution and 8-bit color
plasticbottlesarethemostcommon,whichcanbeattributed depth. The hyperspectral sensor (Specim FX17) is able to
to typical packaging design trends, whereas multicolored capture224contiguousspectralbandsinarangefrom900to
bottlesarerelativelyrare.Glassbottles,ontheotherhand,are 1700 nm. HSI images are stored as data cubes with shape
600×640×224in16-bitprecision.Theauthorsprovidea
generallylessrepresented.Thisdistributionmayaffectmodel
performanceandgeneralizationwithinthebottleclass. detailedsetupofthecamerasystemandtheirpre-processing
The number of labeled objects per image ranges from a includes the alignment of the modalities and cropping
mismatchedareas.RGBandHSIimagesareresizedto256×
singleitemupto15,asshowninFig.8,withmorethan60%
ofimagescontainingthreeorfewerobjects.However,alower 256 pixels and normalized to 32-bit floating-point values in
object count does not necessarily indicate reduced scene the range [0,1] for their model training. Additionally, the
complexity. As illustrated in Fig. 6, even a scene with just datasetismadeavailableinitsoriginal,unprocessedformfor
three objects can be visually complex, featuring substantial furtherexperimentation.
backgroundclutter,occlusions,andbulkywasteitemsonthe
| conveyor | belt. These | factors | present | a significant | challenge |     |               |     |     |     |     |     |     |     |
| -------- | ----------- | ------- | ------- | ------------- | --------- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- |
|          |             |         |         |               |           |     | 2) ANNOTATION |     |     |     |     |     |     |     |
forobjectdetectionalgorithms.Animportantnoteisthatthe The six classes in the presented dataset are defined in
datasetcontainsnoemptyframes,whichmaylimitevaluation
|     |     |     |     |     |     |     | line with | the | requirements | of  | the sorting | facility, | targeting |     |
| --- | --- | --- | --- | --- | --- | --- | --------- | --- | ------------ | --- | ----------- | --------- | --------- | --- |
offalsepositivebehaviorinreal-worldscenarios.
|     |     |     |     |     |     |     | items that | frequently | hinder |     | the efficiency |     | of the | sorting |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ---------- | ------ | --- | -------------- | --- | ------ | ------- |
The class size distribution, as presented in Fig. 4, reveals process.Objectsoftheclassesfilmandbasket arelargeand
| notable | differences | in object | dimensions |     | across | the five |         |        |           |          |          |          |     |       |
| ------- | ----------- | --------- | ---------- | --- | ------ | -------- | ------- | ------ | --------- | -------- | -------- | -------- | --- | ----- |
|         |             |           |            |     |        |          | hard to | break, | likely to | obstruct | conveyor | systems. |     | Video |
maincategories.Thebottle,cardboard,anddetergentclasses
|                                          |         |                     |     |                 |                |        | tape and         | filament | are         | elongated | items  | that     | can entangle |      |
| ---------------------------------------- | ------- | ------------------- | --- | --------------- | -------------- | ------ | ---------------- | -------- | ----------- | --------- | ------ | -------- | ------------ | ---- |
| exhibit                                  | similar | size distributions, |     | with comparable |                | median |                  |          |             |           |        |          |              |      |
|                                          |         |                     |     |                 |                |        | within machinery |          | and require |           | manual | removal. | Closed       | bags |
| areasandvariation.Incontrast,thecanister |         |                     |     |                 | classcomprises |        |                  |          |             |           |        |          |              |      |
containingwasteitemsthatmustbeopenedtoprocessthem,
thelargestobjectsoverallandexhibitsthegreatestvariation areclassifiedastrashbags.Cardboard istheonlyclassthat
insize,reflectingahighdegreeofdiversitywithintheclass.
isslightlyoutoflinebutstillclassified,aspaperobjectshave
Thecansclass,ontheotherhand,containsthesmallestand
arecoveryvalueandaresenttootherrecyclingprocesses.
mostuniformlysizedobjects.
|     |     |     |     |     |     |     | To overcome |         | labor-intensive |     | manual        | polygon | annota- |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ------- | --------------- | --- | ------------- | ------- | ------- | --- |
|     |     |     |     |     |     |     | tion, the   | authors | developed       |     | an annotation | tool    | using   | the |
4) LIMITATIONS point-prompt feature from the Segment Anything Model
The manually annotated bounding boxes are imprecise in (SAM) [32] resulting in high-quality masks that can either
somecases,leavingamargintotheactualobjectboundaries, be refined or directly saved. Annotation is done in the
which can be seen in Fig. 6 and 7. This can reduce RGBimagesonly,resultingin852nonoverlappingannotated
| 151942 |     |     |     |     |     |     |     |     |     |     |     |     | VOLUME13,2025 |     |
| ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------- | --- |

P.Thielmannetal.:ReviewofComputerVisionforIndustrial-GradeWasteClassification
|     |     |     |     | FIGURE10. | NumberofinstancesperimageforSpectralWaste.Seethe |     |     |     |     |
| --- | --- | --- | --- | --------- | ------------------------------------------------ | --- | --- | --- | --- |
Annotationsectionfordetailsoninstancedefinitionforthisdataset.
|     |     |     |     | influenced | by multiple   | factors,  | like the | composition | of the |
| --- | --- | --- | --- | ---------- | ------------- | --------- | -------- | ----------- | ------ |
|     |     |     |     | recorded   | waste stream, | household | waste    | separation  | and    |
collectionpractices,andtheoperationaldesignofthesorting
processitself.Inthedataset,thebagclassisclearlydominant,
|     |     |     |     |                      | film, basket,        |                                | video tape,     |       |           |
| --- | --- | --- | --- | -------------------- | -------------------- | ------------------------------ | --------------- | ----- | --------- |
|     |     |     |     | followed             | by                   | and                            |                 | which | can be    |
|     |     |     |     | considered           | to have intermediate |                                | representation. | In    | contrast, |
|     |     |     |     | filamentandcardboard |                      | appearmorerarely,makingthemthe |                 |       |           |
FIGURE9. SampleImageSpectralWastewithprovidedmaskannotations.
Underscoredclasslabels(e.g.,bag1,bag2)indicatemultipleinstancesof least frequent classes in the dataset. This is summarized in
thesameclassannotatedseparatelywithintheframe.
Table4.Notethatourreportednumberofinstancesperclass
isinlinewithourpreviousassumptionandalsomatchesthe
TABLE4. NumberofinstancesperclassforSpectralWaste.Seethe numbersstatedintheauthorspaper.
Annotationsectionfordetailsoninstancedefinitionforthisdataset. Around 70% of the frames contain between one and
|     |     |     |     | three annotated | instances, | while | frames | with | more than |
| --- | --- | --- | --- | --------------- | ---------- | ----- | ------ | ---- | --------- |
fiveinstancesarerelativelyrare.Notably,theSpectralWaste
datasetalsoincludesframeswithoutanyannotatedinstance,
|     |     |     |     | as visualized       | in Fig. 10. | The           | comparatively  | lower        | number   |
| --- | --- | --- | --- | ------------------- | ----------- | ------------- | -------------- | ------------ | -------- |
|     |     |     |     | of instances        | per frame   | is influenced | by             | the instance | size     |
|     |     |     |     | distribution,       | with the    | relative      | mask area      | of most      | classes  |
|     |     |     |     | being substantially | larger      | than          | those observed | in           | the WaRP |
frames. To automatically transfer the annotated masks to and ZeroWaste datasets, as shown in Fig. 4. Among the
their corresponding objects in the HSI images, a label classes, film generally represents the largest objects and
transferalgorithmwasintroducedthatcompensatesfordata exhibits the greatest intra-class variation in size. Basket is
misalignment resulting from differing camera perspectives thenextsmallerclassinsize.Cardboard andbagfallwithin
and heterogeneous sensor configurations. Annotations are an intermediate size range, though cardboard shows more
availableinmaskformat. variability in object size compared to bag. Video tape and
Further, from our observation, the authors annotated the filament constitutethesmallestclassintermsofobjectsize,
classes film, basket, cardboard, filament, and bag on an whilevideotapehashighermedianandvariationinrelative
| instance-level, | e.g., two     | bags in one      | frame are counted | as maskarea. |     |     |     |     |     |
| --------------- | ------------- | ---------------- | ----------------- | ------------ | --- | --- | --- | --- | --- |
| two instances   | of the class. | The class        | video tape, due   | to its       |     |     |     |     |     |
| elongated       | and tangling  | characteristics, | is always counted | as           |     |     |     |     |     |
4) LIMITATIONS
a single instance, even if the annotated areas are no longer The class video tape contains both the cassette’s magnetic
connected.Thereis,however,oneexceptiontothisrule:video tape and the cassette itself. From a semantic viewpoint this
tape is counted as a single instance only when it refers to is correct, but the visual appearance and characteristics are
themagnetictape(e.g.,fromaVHSoraudiocassette).Ifthe verydifferent,whichcouldlimitsegmentationperformance.
cassetteitselfispresent,itisannotatedasaseparateinstance,
|     |     |     |     | Furthermore, | the video | tape | annotations | are | sometimes |
| --- | --- | --- | --- | ------------ | --------- | ---- | ----------- | --- | --------- |
asitcanbeseeninFig.9. fragmented,likelyreflectinglimitationsofSAM.
| 3) DATASETDETAILS |     |     |     | IV. MODELCOMPARISON |     |     |     |     |     |
| ----------------- | --- | --- | --- | ------------------- | --- | --- | --- | --- | --- |
The SpectralWaste dataset also presents a distinct class ThissectionprovidesanoverviewoftheCVmodelstrained
imbalance, which is characteristic for waste datasets and on the industrial-grade waste datasets presented earlier.
reflects the natural distribution of materials found on a We summarize the reported performance and results of
conveyor belt of a sorting facility. Such imbalances are variousmodelsacrosstheirrespectivetasks–objectdetection
| VOLUME13,2025 |     |     |     |     |     |     |     |     | 151943 |
| ------------- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |

P.Thielmannetal.:ReviewofComputerVisionforIndustrial-GradeWasteClassification
TABLE5. Comparisonofreportedresultsonin-the-wildandindustrial-gradewastedatasetsintheirrespectivetask.Thetablehighlightsthenoticeable
performancegapinindustrialsettings.Forcomparability,wereportrepresentativeresultsratherthanthebest-performingmodelsforeachdataset(e.g.,
DeepLabV3onTACOvs.DeepLabV3+onZeroWaste).
andsemanticsegmentation–alongsideavailablemodeland
1) OBJECTDETECTION
training details. For object detection we state performance The authors of the ZeroWaste dataset reported experiments
resultsinthecommonlyusedAveragePrecision(AP)metric using well-established CNN-based object detectors, includ-
| reflecting | both localization | and | classification | accuracy. | For |     |     |     |     |     |     |     |
| ---------- | ----------------- | --- | -------------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
ingbothtwo-stage(MaskR-CNN[28],TridentNet[33])and
semantic segmentation the Intersection over Union (IoU) is one-stage detectors (RetinaNet [34]). Two-stage detectors
used, measuring the overlap between predicted and ground first generate region proposals and then classify them,
truth segments. AP and IoU are used to evaluate individual whileone-stagedetectorspredictdetectionsinasinglestep,
classes, while mean AP (mAP) and mIoU represent overall reducing inference time and making them suitable for real-
modelperformancebyaveragingacrossallclasses.
|     |     |     |     |     |     | time applications. |     | As shown | in Table | 6,  | all models | struggle |
| --- | --- | --- | --- | --- | --- | ------------------ | --- | -------- | -------- | --- | ---------- | -------- |
Toillustratetheperformancegapofmodelsinindustrial- withthechallengingcharacteristicsofthedataset,achieving
grade settings, we include representative results from in- relatively low mAP performance. All results reported for
the-wild waste datasets in Table 5. These datasets, such objectdetection modelsused theZeroWaste-f subsetsolely.
as TrashNet, TACO, and ReSORT-IT, generally report high Amongtheevaluateddetectionmodelsbytheauthors,Mask
| scores – | e.g., 94.7% classification |     | accuracy | on  | TrashNet, |       |          |           |            |     |        |          |
| -------- | -------------------------- | --- | -------- | --- | --------- | ----- | -------- | --------- | ---------- | --- | ------ | -------- |
|          |                            |     |          |     |           | R-CNN | performs | best when | pretrained |     | on the | TACO [7] |
90.9% mIoU on TACO, and 87.2% mAP on ReSORT-IT. datasetwithamAPscoreof24.32%,highlightingthebenefit
In contrast, industrial-grade datasets such as ZeroWaste, ofdomain-specificpretraininginthewastecontext.
WaRP, and SpectralWaste report markedly lower scores, In a follow-up study, various versions of the YOLO
despitetheuseofcomparableorevenmoreadvancedmodel (You Only Look Once) [43] model were evaluated on the
architectures.
|     |     |     |     |     |     | ZeroWaste | dataset. | YOLO | is a family |     | of one-stage | object |
| --- | --- | --- | --- | --- | --- | --------- | -------- | ---- | ----------- | --- | ------------ | ------ |
Forexample,MaskR-CNN[28]achieves87.2%mAPon detectors that formulates object detection as a regression
ReSORT-IT, but only 24.3% mAP on ZeroWaste. A sim- problem and was continuously improved in terms of speed
ilar trend is seen in semantic segmentation: DeepLabV3 andaccuracyacrossitsgenerations.Theresultsshowaclear
[26] reaches 90.9% mIoU on TACO, while its successor, progression in performance across model generations, with
DeepLabV3+[29],achievesjust52.1%mIoUonZeroWaste.
YOLOv3[35]scoringtheworstandYOLOv7[39]achieving
These discrepancies illustrate the significant challenges thehighestscoresamongthem–especiallyperformingbest
posed by industrial-grade waste data and underscore the indetectingraremetal objects–andrankingthesecond-best
| pressing | need for tailored | model | development | and | bench- |     |     |     |     |     |     |     |
| -------- | ----------------- | ----- | ----------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
reportedmAPof33.2%onZeroWaste-f.
markinginindustrialwasteclassificationtasks. Inaseparatestudy[41],theauthorsinvestigatedmodality
In the following, we summarize reported model per- fusion using a RGB-D dataset for construction and demoli-
formances and training details while highlighting key tionwaste(CDW).FortheZeroWastedataset,however,they
dataset-specific challenges and limitations observed in the estimateddepthinformationfromtheRGBimagesfusingtwo
industrial-gradewastedatasetsZeroWaste,WaRP,andSpec-
|     |     |     |     |     |     | depth estimation |     | methods | using | a depth | merging | network. |
| --- | --- | --- | --- | --- | --- | ---------------- | --- | ------- | ----- | ------- | ------- | -------- |
tralWaste. Theirexperimentsdemonstratedthatincorporatingdepthdata
|     |     |     |     |     |     | boosted | detection | performance | for | ZeroWaste. |     | They also |
| --- | --- | --- | --- | --- | --- | ------- | --------- | ----------- | --- | ---------- | --- | --------- |
showthatlatemodalityfusionissuperiortoearlyfusionand
A. ZEROWASTE
largermodelsfurtherimproveperformance,reachingthebest
| As the first | and most | prominent | industrial-grade |     | waste |     |     |     |     |     |     |     |
| ------------ | -------- | --------- | ---------------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
dataset, ZeroWaste has been explored in numerous studies. mAPscorewith34.25%forobjectdetectiononZeroWaste-f.
|                  |                  |       |         |               |         | The latest   | reported      | results     | for       | the object | detection  | task,      |
| ---------------- | ---------------- | ----- | ------- | ------------- | ------- | ------------ | ------------- | ----------- | --------- | ---------- | ---------- | ---------- |
| However,         | not all of these | works | provide | sufficient    | method- |              |               |             |           |            |            |            |
|                  |                  |       |         |               |         | focusing     | on the        | recognition | of highly |            | deformable | objects    |
| ological details | or transparency  |       | in how  | their results | were    |              |               |             |           |            |            |            |
|                  |                  |       |         |               |         | in cluttered | environments, |             | were      | reported   | in         | [42]. They |
obtained,andthereforearenotincludedinthisreview.
| 151944 |     |     |     |     |     |     |     |     |     |     |     | VOLUME13,2025 |
| ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------- |

P.Thielmannetal.:ReviewofComputerVisionforIndustrial-GradeWasteClassification
TABLE6. ReportedobjectdetectionresultsontheZeroWaste-fdataset.Boldhorizontallinesseparateresultsstatedindifferentsources.Boldvalues
indicatethehighestmAPandAPscoresrespectively.
modify the large-scale CNN-based model InternImage [44] indicatethattheunlabeleddatafromZeroWaste-sdecreased
by incorporating multiscale networks, a combination of the mIoU for ReCo and for CCT it slightly improved
cross-entropy and dice loss for segmentation, and a novel the performance. While CCT performed poorly in both
Freezeconnect module to improve performance. Although settings,ReCoachievedresultscomparabletoDeepLabV3+
DeepLabV3+
no class-wise detection scores are provided, the overall when trained in a fully-supervised manner.
improvement over Mask R-CNN is evident, with a 26.40% was used as baseline for the supervised experiments. The
mAP. model combines atrous convolutions for multiscale feature
|     |     |     |     |     |     |     | extraction  | with    | an encoder-decoder |             | design | to refine | object     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ------- | ------------------ | ----------- | ------ | --------- | ---------- |
|     |     |     |     |     |     |     | boundaries, | showing | a slight           | improvement |        | when      | trained on |
2) SEMANTICSEGMENTATION
In ZeroWaste, the authors conducted their experiments on ZeroWasteAug. The authors noted that the augmentation
semantic segmentation in three approaches – supervised, particularlyimprovedperformanceonthemetalclass,which
|                 |     |                   |     |           |     |         | was underrepresented |     | in  | the original | dataset. | However, | the |
| --------------- | --- | ----------------- | --- | --------- | --- | ------- | -------------------- | --- | --- | ------------ | -------- | -------- | --- |
| semi-supervised | and | weakly-supervised |     | learning. |     | For the |                      |     |     |              |          |          |     |
weakly-supervised experiments, different methods were rigid plastic class experienced a noticeable performance
decline.
| employed | to generate | pseudo-labels |     | based | on Class | Acti- |     |     |     |     |     |     |     |
| -------- | ----------- | ------------- | --- | ----- | -------- | ----- | --- | --- | --- | --- | --- | --- | --- |
vation Maps (CAMs). RISE [45] generates CAMs through The NUNI-Waste [50] method proposes novel data aug-
randomized input masking, estimating pixel importance in mentations–nonuniformcolorandoffsettransformations–
|                  |         |     |              |           |     |      | to simulate | natural | lighting | and | increase | variability, | along |
| ---------------- | ------- | --- | ------------ | --------- | --- | ---- | ----------- | ------- | -------- | --- | -------- | ------------ | ----- |
| a model-agnostic | manner. |     | In contrast, | PuzzleCAM |     | [46] |             |         |          |     |          |              |       |
enhances localization by dividing the image into tiles and with an adaptive loss function to address class imbalance
enforcingconsistencyacrossthem,whileEPS[47]improves andimproveperformanceonrareclasses.UsingU-Net[53],
boundaryaccuracybyincorporatingedgepredictions.These a well-known architecture for semantic segmentation, with
methods were trained on ZeroWaste-w (before-and-after differentbackbonestheauthorsachievebettersegmentation
|             |             |        |         |         |     |          | results than | ZeroWaste |     | and show | that | their methods | also |
| ----------- | ----------- | ------ | ------- | ------- | --- | -------- | ------------ | --------- | --- | -------- | ---- | ------------- | ---- |
| labels) and | ZeroWaste-f | (fully | labeled | images) | to  | generate |              |           |     |          |      |               |      |
DeepLabv3+.
pseudo-labels for training DeepLabV3+ [29]. The results improve performance in The training was
reported in Table 7 show that all weakly-supervised exper- conducted on ZeroWaste-f and ZeroWaste-s, making use of
boththelabeledandtheprovidedunlabeleddata–beingthe
| iments performed | poorly, |     | with EPS | reaching | the | highest |     |     |     |     |     |     |     |
| ---------------- | ------- | --- | -------- | -------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
mIoU of 34.06% among them. For the semi-supervised onlyapproachthatachievedimprovementsoverthebaseline
byleveragingtheunlabeledsubset.
| experiments, | the authors | used | CCT | [48] | and ReCo | [49] |     |     |     |     |     |     |     |
| ------------ | ----------- | ---- | --- | ---- | -------- | ---- | --- | --- | --- | --- | --- | --- | --- |
on ZeroWaste-s and ZeroWaste-f, combining labeled and Theauthorsof[42]trainedtheirmodifiedInternImage[44]
unlabeled data. ReCo leverages both local and global version not only for object detection but also for semantic
segmentation,achievingbetterscoresthantheDeepLabV3+
| context along | with a | Mean | Teacher | framework | for | pseudo- |     |     |     |     |     |     |     |
| ------------- | ------ | ---- | ------- | --------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
labeling,whileCCTenforcesconsistencyacrossaugmented baseline, although they drastically increased the number of
epochsfortraining.
| views to      | guide training | on  | unlabeled | examples. | The | results |     |     |     |     |     |     |        |
| ------------- | -------------- | --- | --------- | --------- | --- | ------- | --- | --- | --- | --- | --- | --- | ------ |
| VOLUME13,2025 |                |     |           |           |     |         |     |     |     |     |     |     | 151945 |

P.Thielmannetal.:ReviewofComputerVisionforIndustrial-GradeWasteClassification
TABLE7. ReportedsemanticsegmentationresultsontheZeroWastedataset.Boldhorizontallinesseparateresultsstatedindifferentsources.Bold
valuesindicatethehighestmIoUandIoUscoresrespectively.
.
Following the path of model adaptation to the specific 3) KEYCHALLENGES
| waste domain, | in [52] | a new backbone | architecture | called |               |         |                             |      |
| ------------- | ------- | -------------- | ------------ | ------ | ------------- | ------- | --------------------------- | ---- |
|               |         |                |              |        | The ZeroWaste | dataset | presents several challenges | that |
FeatureAmplificationNetwork(FANet)wasintroduced.The impactdetectionandsegmentationperformance.Strongclass
authors focus on preserving both low- and high-frequency imbalancemakesitdifficultformodelstolearnlessfrequent
features within their hierarchical backbone, employing a classes like rigid plastic and metal, an issue worsened by
series of specially designed blocks to improve semantic their smaller object sizes compared to cardboard and soft
| segmentation | performance | in cluttered | environments. | With |     |     |     |     |
| ------------ | ----------- | ------------ | ------------- | ---- | --- | --- | --- | --- |
plastic.Distinguishingbetweensoftplasticandrigidplastic
visual comparisons, they show improved results for soft is especially challenging due to their highly similar visual
plastic and segmentation of objects with strong background textures and appearances. Brown paper objects, labeled as
clutter. In comparison to FocalNet [51] – a recent vision background,areoftenclassifiedascardboard havingalmost
transformer known for its strong performance in segmen- identicalshapeandcolor–mainlydifferentiablebynonvisual
tation tasks – they demonstrate superior results, outper- metal
|     |     |     |     |     | features | like thickness | and rigidity. Moreover, | and |
| --- | --- | --- | --- | --- | -------- | -------------- | ----------------------- | --- |
forming both FocalNet and the ZeroWaste baseline with a plasticobjectswithsimilarcolorand/orhighreflectanceare
mIoU of 54.89%, all while using a more compact model frequentlymisclassified.
architecture.
| The most | recent model | evaluated | on ZeroWaste, | named |     |     |     |     |
| -------- | ------------ | --------- | ------------- | ----- | --- | --- | --- | --- |
COSNet (Cluttered Objects Semantic Segmentation Net- 4) LIMITATIONS
work)[31],introducesaspecializedarchitecturedesignedto WhiletheZeroWaste-wsubsetwithbefore-and-afterhuman
handle the challenges of cluttered environments. By lever- sorting images is a promising idea to learn a model in a
aging multiscale features from a hierarchical backbone, weakly-supervisedmannerwhichobjectsaresortedout,ithas
it employs Feature Sharpening Blocks to enhance both not been utilized in any subsequent study – questioning the
contextual understanding and object boundary delineation. suitability ofthis subset for theintended task. This leadsus
toassumptionswhythissubsetcouldhavefaileditspurpose:
| Additionally, | a dedicated | Boundary       | Enhancement | Module       |     |     |     |     |
| ------------- | ----------- | -------------- | ----------- | ------------ | --- | --- | --- | --- |
| refines these | features    | before passing | them to     | the decoder, |     |     |     |     |
resulting in improved IoU scores across all classes – before-andafter-framesarenotalignedtoeachother
•
most notably for rigid plastic. Reporting the highest • before- and after-frames have different resolution,
mIoU with 56.77% reached for semantic segmentation on indicating slightly different camera mounting or setup
| ZeroWaste. |     |     |     |     | introducingadomainshift |     |               |     |
| ---------- | --- | --- | --- | --- | ----------------------- | --- | ------------- | --- |
| 151946     |     |     |     |     |                         |     | VOLUME13,2025 |     |

P.Thielmannetal.:ReviewofComputerVisionforIndustrial-GradeWasteClassification
TABLE8. ReportedobjectdetectionresultsontheWaRPdataset.EachrowrepresentsAPscoresforthe28subcategoriesandAPscoresforthe5merged
categorieswiththevaluesshowninbrackets.BoldvaluesindicatethehighestmAPandAPscoresrespectively.
• act of human sorting disrupts object positions on the to the lack of clearly reported results or sufficient training
| conveyor |     |     |     | details. |     |     |     |
| -------- | --- | --- | --- | -------- | --- | --- | --- |
Thesepointsmakethealreadychallengingtaskofweakly-or 1) OBJECTDETECTION
self-supervisedlearningevenmorechallenging. Asabaseline,severalexperimentsondifferentobjectdetec-
We can derive similar findings for the ZeroWasteAug tion models were performed with a focus on low computa-
subset. While augmenting rare classes is generally a useful tionalcostandreal-timecapability.Theexperimentsincluded
strategy to address class imbalances, in this case, the one-stage detection models (YOLOv3 [35], YOLOv5 [38],
augmentation of metal and rigid plastic objects from the YOLOX[56],CenterNet[55],ATSS[54],TOOD[30]),two-
TACO[7]datasetimposesadomainshiftitself–transitioning stage detection models (Faster R-CNN [57], Dynamic R-
fromin-the-wildwasteobjectstoindustrial-grademunicipal CNN [58], Sparse R-CNN [59]) and a transformer archi-
wasteobjects.Thismayexplainwhyotherresearchershave tecture (D-DETR [60]). The authors trained the models on
the28subcategoriesandthe5jointcategories,respectively.
| avoided using | this subset | to train their models, | as the best |     |     |     |     |
| ------------- | ----------- | ---------------------- | ----------- | --- | --- | --- | --- |
performanceswereachievedusingthenonaugmentedversion As shown in Table 8, the performance difference in overall
ofthedataset. mAP between the two setups is model-specific, with no
While some methods incorporate the unlabeled data, consistenttrend.However,theclass-wiseAPvaluesindicate
the best-performing models tend not to, raising the ques- thatjoiningthesubcategoriesfromthebottle,cardboard,and
|                 |             |                |            | detergent class, | respectively, | improves performance | across |
| --------------- | ----------- | -------------- | ---------- | ---------------- | ------------- | -------------------- | ------ |
| tion of whether | the complex | classification | rules make |                  |               |                      |        |
pseudo-labelingcounterproductive–possiblyevendegrading all models – especially for the bottle class. For the more
performance. detailed category structure, the one-stage detectors TOOD
|         |     |     |     | and YOLOX-m                                         | performed | the best with 60.2%  | and 58.6%   |
| ------- | --- | --- | --- | --------------------------------------------------- | --------- | -------------------- | ----------- |
|         |     |     |     | mAP, respectively.                                  | For the   | simplified and joint | categories, |
| B. WARP |     |     |     | thetransformer-basedD-DETRachievedthehighestperfor- |           |                      |             |
In the WaRP [9] dataset, the authors investigated a hier- mancewith58.9%mAP,followedbyYOLOX-mwith58.3%.
| archical detection | approach | by using a detection | model to |     |     |     |     |
| ------------------ | -------- | -------------------- | -------- | --- | --- | --- | --- |
output the bounding box of an object and a classification 2) KEYCHALLENGES
modeltodeterminetheclassofthedetectedobject.Sincewe The cardboard and detergent categories proved to be the
compare on the object detection and semantic segmentation most challenging for object detection, achieving the lowest
tasks and not on classification, we note only the results of AP scores across all models. For cardboard, the difficulty
the evaluated detection models. Furthermore, we excluded likely stems from the wide variety of beverage container
additional papers citing WaRP from our comparison due designs for milk and juice and the severe deformations
| VOLUME13,2025 |     |     |     |     |     |     | 151947 |
| ------------- | --- | --- | --- | --- | --- | --- | ------ |

P.Thielmannetal.:ReviewofComputerVisionforIndustrial-GradeWasteClassification
TABLE9. ReportedsemanticsegmentationresultsontheSpectralWastedataset.Boldhorizontallinesseparateresultsstatedindifferentsources.Bold
valuesindicatethehighestmIoUandIoUscoresrespectively.
.
these items often undergo after use. In the detergent reportedimprovedperformanceformodalityfusionofRGB
category,challengesarisenotonlyfromthediversityincolor andHSIdata.TheHSIdataisusedintwodifferentvariants:
schemes but also from the substantial variation in shape, HYPER all hyperspectral bands serve as input; HYPER3
ranging from rectangular boxes to bottle-like or shampoo- the 224 channels are reduced to three channels through
stylecontainers.Thesefactorsincreaseintra-classvariability PrincipalComponentAnalysis(PCA).Thefirstexperiments
and make it harder for models to learn consistent visual on MiniNet-v2 [61], a lightweight CNN-based semantic
patterns, suggesting that both higher intra-class diversity segmentation model, and SegFormer [62], a transformer-
anddeformationcontributesignificantlytoreduceddetection based model with a hierarchical encoder and a light-weight
performance.Accordingly,detectionscoresforcans,witha MLPdecoderavailableindifferentmodelsizes,showedthat
lowerintra-classvariabilityindesignandsize,arerelatively bothversionsofhyperspectraldataimprovedthemIoUscores
high,despitepresentingthesmallestobjects. compared to training with RGB-only data (see Table 9).
|     |     |     |     |     |     |     |     | While not | all classes | are | improving, | it      | can | be clearly   | seen |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | ----------- | --- | ---------- | ------- | --- | ------------ | ---- |
|     |     |     |     |     |     |     |     | that the  | cardboard   | and | filament   | classes | can | be segmented |      |
3) LIMITATIONS
|     |     |     |     |     |     |     |     | much better | using | HSI | data. The | authors | [10] | investigated |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ----- | --- | --------- | ------- | ---- | ------------ | --- |
Theauthorsdidnotprovideanytrainingdetailsforthedetec-
|     |     |     |     |     |     |     |     | modality | fusion | by evaluating |     | CMX | [63], | a multimodal |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ------ | ------------- | --- | --- | ----- | ------------ | --- |
tionmodels,whichmakesfaircomparisonoffuturemodels
|          |              |     |            |             |     |     |         | transformer | fusing | RGB | and auxiliary |     | data | combined | with |
| -------- | ------------ | --- | ---------- | ----------- | --- | --- | ------- | ----------- | ------ | --- | ------------- | --- | ---- | -------- | ---- |
| hard and | reproduction |     | of results | impossible. |     | As  | already |             |        |     |               |     |      |          |      |
across-modalattentionmechanism.WhileCMXemploysa
| stated in    | the dataset  |              | comparison,  | some       | of         | the bounding |          |               |              |         |                |          |                 |                |        |
| ------------ | ------------ | ------------ | ------------ | ---------- | ---------- | ------------ | -------- | ------------- | ------------ | ------- | -------------- | -------- | --------------- | -------------- | ------ |
|              |              |              |              |            |            |              |          | hybrid fusion | strategy,    |         | for MiniNet-v2 |          | and             | SegFormer      | the    |
| boxes are    | imprecise    |              | leaving      | a gap      | to the     | actual       | object   |               |              |         |                |          |                 |                |        |
|              |              |              |              |            |            |              |          | authors       | used a       | simpler | approach       | in       | which           | the modalities |        |
| boundaries.  | This         | can          | lead to      | unreliable | evaluation |              | results, |               |              |         |                |          |                 |                |        |
|              |              |              |              |            |            |              |          | are just      | concatenated |         | before         | being    | input           | to the         | model. |
| where models |              | that predict | tighter,     |            | more       | accurate     | boxes    |               |              |         |                |          |                 |                |        |
|              |              |              |              |            |            |              |          | The modality  | fusion       | for     | SegFormer      |          | and MinitNet-v2 |                | did    |
| around       | the object   | might        | receive      | lower      | scores     | compared     |          |               |              |         |                |          |                 |                |        |
|              |              |              |              |            |            |              |          | not improve   | the          | mIoU    | scores         | compared |                 | to the         | HYPER  |
| to models    | whose        | predictions  |              | more       | loosely    | align        | with the |               |              |         |                |          |                 |                |        |
|              |              |              |              |            |            |              |          | experiments.  | However,     |         | CMX            | showed   | the best        | performance    |        |
| imprecise    | annotations. |              | Furthermore, |            | grouping   | plastic      | and      |               |              |         |                |          |                 |                |        |
onRGB-HYPERwith58.2%mIoU,andalsoforthereduced
| glass bottle | objects      | into      | a joint   | category | is             | debatable, | as it      |               |      |            |           |       |                 |     |         |
| ------------ | ------------ | --------- | --------- | -------- | -------------- | ---------- | ---------- | ------------- | ---- | ---------- | --------- | ----- | --------------- | --- | ------- |
|              |              |           |           |          |                |            |            | hyperspectral | data | it exceeds | the       | other | models.         | The | authors |
| merges       | two distinct | materials |           | and thus | limits         | the        | ability to |               |      |            |           |       |                 |     |         |
|              |              |           |           |          |                |            |            | reason that   | the  | imperfect  | alignment | of    | both modalities |     | adds    |
| assess the   | capacity     | of        | CV models |          | to distinguish |            | between    |               |      |            |           |       |                 |     |         |
noise,thuslimitingtheearly-fusion,whilethehybrid-fusion
visuallysimilarobjectsmadeofdifferentmaterials.
methodCMXcanlearnandsmoothoutthisnoise.
|     |     |     |     |     |     |     |     | The authors |     | of the COSNet |     | [31] model | also | tested | their |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ------------- | --- | ---------- | ---- | ------ | ----- |
C. SPECTRALWASTE model on SpectralWaste and compared it with FANet [52]
1) SEMANTICSEGMENTATION andInternImage[44],alltrainedonRGB-onlydata.Adirect
Several experiments have been conducted by the authors comparison to the SpectralWaste baseline results is not
entirelyfair,astheyusedhigherresolutiondatafortraining
| of the SpectralWaste |     | [10] | dataset, | focusing |     | on efficient | and |     |     |     |     |     |     |     |     |
| -------------------- | --- | ---- | -------- | -------- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
real-time capable models. For semantic segmentation they and employed larger model architectures. Nonetheless,
| 151948 |     |     |     |     |     |     |     |     |     |     |     |     |     | VOLUME13,2025 |     |
| ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------- | --- |

P.Thielmannetal.:ReviewofComputerVisionforIndustrial-GradeWasteClassification
they achieved the highest mIoU score with 69.96% and tailored to the waste sorting environment, outperforming
demonstrated the effectiveness of their specialized model standardoff-the-shelfmodelsthatlacksuchspecialization.
in cluttered environments. It should also be noted that they A broader issue in the waste classification research land-
reachedaveryhighIoUinthefilamentclass,whereprevious scapeisthelackofstandardswhenreportingandevaluating
models struggled – especially the models trained solely on results. Inconsistent documentation of experimental setups,
RGB data. This indicates that the smallest class filament in such as training parameters, model size and backbone
size, benefits from using higher resolution images as input. pretraining, hinders fair comparison and reproducibility.
VideotapeistheclasswiththelowestIoUshowingagapto Moreover, the absence of public codebases in some cases
theotherwell-segmentedclasses. makesitimpossibletovalidateorbuilduponpriorwork.
|     |     |     |     |     |     |     |     | V. FUTUREDIRECTIONS |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------- | --- | --- | --- | --- | --- | --- |
2) KEYCHALLENGES
Inthissection,wewilldiscussfutureresearchdirectionsthat
| While filament | proved |     | to be the | most    | challenging |     | class for |          |           |          |        |          |            |      |
| -------------- | ------ | --- | --------- | ------- | ----------- | --- | --------- | -------- | --------- | -------- | ------ | -------- | ---------- | ---- |
|                |        |     |           |         |             |     |           | have the | potential | to solve | one or | multiple | challenges | that |
| nonspecialized | models |     | due to    | its low | number      | of  | instances |          |           |          |        |          |            |      |
occurinindustrial-gradewasteclassification.
| and the small,         | thin,              | and  | elongated | visual | appearance, |              | spe- |                     |     |              |            |     |         |          |
| ---------------------- | ------------------ | ---- | --------- | ------ | ----------- | ------------ | ---- | ------------------- | --- | ------------ | ---------- | --- | ------- | -------- |
| cialized architectures |                    | like | FANet     | and    | COSNet      | successfully |      |                     |     |              |            |     |         |          |
|                        |                    |      |           |        |             |              |      | 1) FOUNDATIONMODELS |     |              |            |     |         |          |
| addressed              | these difficulties |      | by        | using  | higher      | resolution   | data |                     |     |              |            |     |         |          |
|                        |                    |      |           |        |             |              |      | As we can           | see | in the Model | Comparison |     | Section | the most |
forthesemodels.However,evenforspecializedmodels,the
segmentation of video tape, with its translucent and partial recentandwell-performingmodelsareadaptedmethodsand
specializedarchitecturestoenhanceperformanceincluttered
| visual appearance, |     | remains | challenging |     | and | represents | an  |     |     |     |     |     |     |     |
| ------------------ | --- | ------- | ----------- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
environmentsandthewastedomain.Meanwhile,thebroader
openproblem.Additionally,thefusionofmultiplemodalities
|     |     |     |     |     |     |     |     | CV field | is shifting | toward | foundation |     | models | trained |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ----------- | ------ | ---------- | --- | ------ | ------- |
stillrequiresfurtherinvestigationtofullyrealizeitspotential.
|     |     |     |     |     |     |     |     | on large-scale |               | datasets, | offering         | strong | generalization | and |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | ------------- | --------- | ---------------- | ------ | -------------- | --- |
|     |     |     |     |     |     |     |     | zero-shot      | capabilities, | reaching  | state-of-the-art |        | performance    |     |
3) LIMITATIONS
|     |     |     |     |     |     |     |     | across multiple |     | tasks and | datasets. | Despite |     | this trend, |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------- | --- | --------- | --------- | ------- | --- | ----------- |
ApotentiallimitationoftheSpectralWastedatasetarisesfrom foundation models remain largely untapped in the waste
thelow-resolutioninputusedforthemodalityfusion,which
domain.
maybeconstrainedbymisalignmentacrossthesensorsand
theneedtocropnonoverlappingareasofthemodalities.Asa
|             |          |     |            |     |       |     |          | 2) ANNOTATIONBOTTLENECK |     |     |     |     |     |     |
| ----------- | -------- | --- | ---------- | --- | ----- | --- | -------- | ----------------------- | --- | --- | --- | --- | --- | --- |
| result, the | original | HSI | resolution | of  | 600 × | 640 | might be |                         |     |     |     |     |     |     |
Thehighannotationeffortforindustrial-gradewastedatasets
effectively reduced, potentially limiting modality fusion at leads to small-sized datasets and in general a lower number
| higher resolutions. |        | Further | experiments |      | using    | larger | models |             |           |     |              |       |     |             |
| ------------------- | ------ | ------- | ----------- | ---- | -------- | ------ | ------ | ----------- | --------- | --- | ------------ | ----- | --- | ----------- |
|                     |        |         |             |      |          |        |        | of datasets | published | in  | this domain. | While | the | integration |
| for modality        | fusion | would   | have        | been | valuable | to     | assess |             |           |     |              |       |     |             |
ofsegmentationmodelslikeSAMintheannotationprocess
thetrade-offbetweenincreasedinferencetimeandpotential makes labor-intensive manual mask drawings obsolete, the
gainsinsegmentationaccuracy.
|     |     |     |     |     |     |     |     | labeling | to specific | guidelines | is        | still challenging |     | and often   |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ----------- | ---------- | --------- | ----------------- | --- | ----------- |
|     |     |     |     |     |     |     |     | requires | expert      | knowledge  | or expert | reviews.          | A   | data engine |
D. SYNTHESIS as used in SAM [32] to generate a huge dataset, could
Thedetailedmodelcomparisonandanalysisofthereported mitigatethisbystartingwithasmallernumberofannotated
|                  |      |      |         |       |        |            |     | frames and | increasing |     | the number | of  | annotated | frames |
| ---------------- | ---- | ---- | ------- | ----- | ------ | ---------- | --- | ---------- | ---------- | --- | ---------- | --- | --------- | ------ |
| results indicate | that | each | dataset | poses | unique | challenges |     |            |            |     |            |     |           |        |
but also that some similarities are shared. The cluttered throughmodel-assistedannotations–basedonthefirstsmall
scenes with deformed, translucent and occluded objects on annotated dataset – combined with human intervention in
the conveyor belt seem to be the main challenge for all multiple iterations. Another way could be the integration of
industrial-grade waste datasets for the investigated object open-vocabularymethods,suchasCLIP[64],toautomatethe
detectionandsegmentationmodels.InthecaseofZeroWaste, labelingofobjectssegmentedinframes.
| class definition | depends |     | on material |     | properties, | making | it  |     |     |     |     |     |     |     |
| ---------------- | ------- | --- | ----------- | --- | ----------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
difficulttodifferentiatebetweenmaterialswithsimilarvisual 3) SELF-SUPERVISEDLEARNING
features, such as soft plastic and rigid plastic. In contrast, Aligned with the goal of reducing annotation effort,
the WaRP and SpectralWaste datasets rely on both material self-supervised learning holds significant promise for
and object-level classification, where certain object classes industrial-grade waste classification. Given that data
with high visual variability pose additional challenges for acquisitionfromconveyorbeltsystemsisrelativelystraight-
CV models. For more challenging classes, performance is forward, and that datasets like ZeroWaste and Spectral-
also correlated with class frequency, as rare categories tend Waste include substantial unlabeled subsets, this approach
to achieve significantly lower scores. This finding clearly remainsunderexplored.Futureworkshouldinvestigatehow
indicates the need for a future dataset with a larger number self-supervised techniques can be leveraged to learn robust
ofinstancesinthechallengingclasses. representations from unlabeled data, potentially improving
The well-performing models demonstrate a clear trend model performance without the need for excessive manual
| towarddomain-specificadaptationsandcustomarchitectures |     |     |     |     |     |     |     | annotation. |     |     |     |     |     |        |
| ------------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- | ------ |
| VOLUME13,2025                                          |     |     |     |     |     |     |     |             |     |     |     |     |     | 151949 |

P.Thielmannetal.:ReviewofComputerVisionforIndustrial-GradeWasteClassification
4) SYNTHETICDATA classification. We began by positioning our contribution
Theeffectiveapplicationofsyntheticdatatoenhancemodel within the landscape of existing reviews in the field of
performance by providing more training data or equalizing waste classification, identifying a notable gap: the absence
class imbalances remains an open challenge. While the of reviews focused specifically on industrial-grade datasets
SynthWaste dataset was published in the VisDA2022 Chal- and state-of-the-art CV models for municipal solid waste
lenge[15],itwasnotusedbytop-performingmethodsdueto sorting. To bridge this gap, we presented the first, to our
insufficientrealismofthesyntheticdata.However,generat- knowledge, in-depth analysis of industrial-grade waste
ing more realistic synthetic data of waste on conveyor belts datasets,examiningtheirclassificationschemes,challenges,
holdsstrongpotentialtoimprovemodelperformance,lower andlimitations,andclearlydistinguishingthemfromin-the-
the amount of annotated data and enhance generalization wild waste datasets. Building on this, we compared models
acrossdomainshiftscausedbyseasonalchangesorvarying trained and evaluated on these datasets and presented a
sortingfacilities.Moreover,domainadaptationmethodscan consolidated overview of reported performances to support
beexploredtobridgelargerdomainshiftsbetweensynthetic future benchmarking and model development. Our analysis
andrealdata. highlights that cluttered scenes and deformed and occluded
objectsremainthemajorchallenge,whileindividualdatasets
posefurtherchallengesduetotheirspecialapplication-based
5) MODALITYFUSION
classification schemes. Furthermore, a trend of top-
The first multimodal, industrial-grade waste dataset Spec-
performing models, favoring domain-specific adaptations
tralWaste demonstrated the potential of modality fusion
overgenericarchitectures,wasdiscovered.However,thelack
approaches in this domain. Although the top-performing
ofstandardizedreportingandmissingcodebasescontinuesto
modelstrainedonhigherresolutionRGB-onlydata–making
hinder fair comparison, reproducibility, and progress in the
direct comparison with fused approaches challenging – the
field. Finally, we outlined key research directions, such as
fusion of RGB with HSI or NIR modalities remains a
the use of foundation models and self-supervised learning,
promising direction. This is particularly relevant for plastic
generationofrealisticsyntheticdataanddomainadaptation,
waste sorting, where a distinction between plastic materials
as well as modality fusion, that should be investigated to
is necessary for proper recycling. Notably, NIR sensors
enhanceindustrial-gradewasteclassification.
are already widely deployed in real-world sorting facilities,
which underscores the practical relevance of investigating
modality fusion further. In addition, the incorporation of ACKNOWLEDGMENT
TheauthorsusedChatGPT,alanguagemodeldevelopedby
other modalities, such as depth information, could help
OpenAI, to assist with language editing and improving the
mitigatechallengescausedbyocclusioninclutteredconveyor
clarityandstructureofthemanuscript.Allscientificcontent
belt scenes and should be further explored in future
wascreatedandvalidatedbythem.
research.
REFERENCES
6) INDUSTRYAPPLICATION
[1] Beyond Age Waste: Turning Rubbish Into a Resource, Global Waste
Beyond academic benchmarks, computer vision models
ManagementOutlook,UNEP,Nairobi,Kenya,2024.
for waste classification must ultimately prove effective in
[2] S. P. Gundupalli, S. Hait, and A. Thakur, ‘‘A review on automated
real-world industrial sorting facilities, where high through- sorting of source-separated municipal solid waste for recycling,’’
put, strict latency constraints and robustness are critical. Waste Manage., vol. 60, pp.56–74, Feb. 2017. [Online]. Available:
https://linkinghub.elsevier.com/retrieve/pii/S0956053X16305189
For example, when interfaced with robotic sorting systems,
[3] N. Kroell, X. Chen, K. Greiff, and A. Feil, ‘‘Optical
visionoutputsmustnotonlyachievehighaccuracybutalso sensors and machine learning algorithms in sensor-based
deliver predictions with low inference times to keep pace material flow characterization for mechanical recycling
processes: A systematic literature review,’’ Waste Manage.,
with fast-moving conveyor belts. Moreover, outputs should
vol. 149, pp.259–290, Jul. 2022. [Online]. Available:
be actionable for downstream actuation: in robotic pick- https://linkinghub.elsevier.com/retrieve/pii/S0956053X22002628
and-place systems, this involves supporting grasp planning [4] W. Lu and J. Chen, ‘‘Computer vision for solid waste sorting: A
critical review of academic research,’’ Waste Manage., vol. 142,
by accounting for object shape, material properties, and
pp.29–43, Apr. 2022. [Online]. Available: https://linkinghub.
occlusion.[65]Futureworkshouldthereforeaddressnotonly elsevier.com/retrieve/pii/S0956053X22000678
accuracybutalsoinferencespeedandrobustnesstoindustrial [5] D. Bashkirova, M. S. Abdelfattah, Z. Zhu, J. Akl, F. Alladkani,
P. Hu, V. Ablavsky, B. Çalli, S. A. Bargal, and K. Saenko,
conditions, enabling reliable integration of computer vision
‘‘ZeroWaste dataset: Towards deformable object segmentation in
modelsintoroboticandautomatedsortingprocessesatscale. cluttered scenes,’’ in Proc. IEEE/CVF Conf. Comput. Vis. Pattern
Recognit., Jun. 2022, pp. 21147—21157. [Online]. Available:
https://openaccess.thecvf.com/content/CVPR2022/html/Bashkirova_
VI. CONCLUSION ZeroWaste_Dataset_Towards_Deformable_Object_
This review addressed the rapidly evolving field of Segmentation_in_Cluttered_Scenes_CVPR_2022_paper.html
industrial-grade waste classification of municipal solid [6] M.YangandG.Thung,ClassificationofTrashforRecyclabilityStatus,
documentCS229ProjectRep.,2016.
waste through a comprehensive, CV–oriented perspective
[7] P.FProençaandP.Simões,‘‘TACO:Trashannotationsincontextforlitter
both on existing datasets and published models for waste detection,’’2020,arXiv:2003.06975.
151950 VOLUME13,2025

P.Thielmannetal.:ReviewofComputerVisionforIndustrial-GradeWasteClassification
[8] M.Koskinopoulou,F.Raptopoulos,G.Papadopoulos,N.Mavrakis,and [24] L.Sharan,R.Rosenholtz,andE.H.Adelson,‘‘Accuracyandspeedof
M.Maniadakis,‘‘Roboticwastesortingtechnology:Towardavision-based materialcategorizationinreal-worldimages,’’J.Vis.,vol.14,no.9,p.12,
categorizationsystemfortheindustrialroboticseparationofrecyclable Aug.2014,doi:10.1167/14.9.12.
waste,’’IEEERobot.Autom.Mag.,vol.28,no.2,pp.50–60,Jun.2021. [25] F.S.Alrayes,M.M.Asiri,M.S.Maashi,M.K.Nour,M.Rizwanullah,
[Online].Available:https://ieeexplore.ieee.org/document/9395690/ A.E.Osman,S.Drar,andA.S.Zamani,‘‘Wasteclassificationusingvision
|               |     |             |     |           |     |          |           | transformer | based | on multilayer |     | hybrid convolution |     | neural network,’’ |
| ------------- | --- | ----------- | --- | --------- | --- | -------- | --------- | ----------- | ----- | ------------- | --- | ------------------ | --- | ----------------- |
| [9] D. Yudin, | N.  | Zakharenko, | A.  | Smetanin, | R.  | Filonov, | M.Kichik, |             |       |               |     |                    |     |                   |
UrbanClimate,vol.49,May2023,Art.no.101483.[Online].Available:
| V.  | Kuznetsov, | D. Larichev, |     | E. Gudov, | S.  | Budennyy, | and |     |     |     |     |     |     |     |
| --- | ---------- | ------------ | --- | --------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
A.Panov, ‘‘Hierarchical waste detection with weakly supervised https://www.sciencedirect.com/science/article/pii/S2212095523000779
segmentation in images from recycling plants,’’ Eng. Appl. Artif. [26] L.-C.Chen,G.Papandreou,F.Schroff,andH.Adam,‘‘Rethinkingatrous
Intell., vol. 128, Feb. 2024, Art.no.107542. [Online]. Available: convolutionforsemanticimagesegmentation,’’2017,arXiv:1706.05587.
https://linkinghub.elsevier.com/retrieve/pii/S0952197623017268 [27] T.Wang,Y.Cai,L.Liang,andD.Ye,‘‘Amulti-levelapproachtowaste
objectsegmentation,’’Sensors,vol.20,no.14,p.3816,Jul.2020.[Online].
| [10] S. Casao, | F.  | Peña, A. Sabater, | R.  | Castillón, | D. Suárez, | E.Montijano, |     |     |     |     |     |     |     |     |
| -------------- | --- | ----------------- | --- | ---------- | ---------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
Available:https://www.mdpi.com/1424-8220/20/14/3816
| and     | A. C. Murillo, | ‘‘SpectralWaste |                | dataset: | Multimodal | data           | for waste |             |     |           |            |     |              |           |
| ------- | -------------- | --------------- | -------------- | -------- | ---------- | -------------- | --------- | ----------- | --- | --------- | ---------- | --- | ------------ | --------- |
|         |                |                 |                |          |            |                |           | [28] K. He, | G.  | Gkioxari, | P. Dollár, | and | R. Girshick, | ‘‘Mask R- |
| sorting | automation,’’  | in              | Proc. IEEE/RSJ |          | Int. Conf. | Intell. Robots | Syst.     |             |     |           |            |     |              |           |
(IROS),Oct.2024,pp.5852–5858.[Online].Available:https://ieeexplore. CNN,’’ in Proc. IEEE Int. Conf. Comput. Vis. (ICCV), Oct. 2017,
ieee.org/abstract/document/10801797 pp.2980–2988. [Online]. Available: https://openaccess.thecvf.
com/content_iccv_2017/html/He_Mask_R-
| [11] M. | Abdallah, | M. A. Talib, | S.  | Feroz, | Q. Nasir, | H. Abdalla, | and |     |     |     |     |     |     |     |
| ------- | --------- | ------------ | --- | ------ | --------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
CNN_ICCV_2017_paper.html
| B. Mahfood, |     | ‘‘Artificial | intelligence | applications |       | in solid waste | man-      |                   |       |         |                |           |             |              |
| ----------- | --- | ------------ | ------------ | ------------ | ----- | -------------- | --------- | ----------------- | ----- | ------- | -------------- | --------- | ----------- | ------------ |
|             |     |              |              |              |       |                |           | [29] L.-C.        | Chen, | Y. Zhu, | G. Papandreou, |           | F. Schroff, | and H. Adam, |
| agement:    | A   | systematic   | research     | review,’’    | Waste | Manage.,       | vol. 109, |                   |       |         |                |           |             |              |
|             |     |              |              |              |       |                |           | ‘‘Encoder–decoder |       | with    | atrous         | separable | convolution | for semantic |
pp.231–246,May2020.[Online].Available:https://linkinghub.elsevier.
com/retrieve/pii/S0956053X20302269 image segmentation,’’ in Proc. Eur. Conf., 2018, pp.833–851.
|     |     |     |     |     |     |     |     | [Online]. | Available: |     | https://openaccess.thecvf.com/content_ECCV_ |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | ---------- | --- | ------------------------------------------- | --- | --- | --- |
[12] L. Andeobu, S. Wibowo, and S. Grandhi, ‘‘Artificial intelligence 2018/html/Liang-Chieh_Chen_Encoder-Decoder_with_Atrous_ECCV_
| applications |     | for sustainable | solid | waste | management |     | practices |     |     |     |     |     |     |     |
| ------------ | --- | --------------- | ----- | ----- | ---------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
2018_paper.html
| in   | australia: | A systematic |                | review,’’ | Sci.      | Total | Environ.,  |               |           |           |         |              |        |                |
| ---- | ---------- | ------------ | -------------- | --------- | --------- | ----- | ---------- | ------------- | --------- | --------- | ------- | ------------ | ------ | -------------- |
|      |            |              |                |           |           |       |            | [30] C. Feng, | Y. Zhong, | Y.        | Gao, M. | R. Scott,    | and W. | Huang, ‘‘TOOD: |
| vol. | 834,       | Aug. 2022,   | Art.no.155389. |           | [Online]. |       | Available: |               |           |           |         |              |        |                |
|      |            |              |                |           |           |       |            | Task-aligned  |           | one-stage | object  | detection,’’ | in     | Proc. IEEE/CVF |
https://linkinghub.elsevier.com/retrieve/pii/S0048969722024822 Int. Conf. Comput. Vis. (ICCV),
|     |     |     |     |     |     |     |     |     |     |     |     | Oct. | 2021, | pp.3490–3499. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | ----- | ------------- |
[13] T.-W. Wu, H. Zhang, W. Peng, F. Lü, and P.-J. He, ‘‘Applications [Online]. Available: https://www.computer.org/csdl/proceedings-
of convolutional neural networks for intelligent waste identification article/iccv/2021/281200d490/1BmEvqSJIEE
and recycling: A review,’’ Resour., Conservation Recycling, vol. 190, [31] M. Ali, M. Javaid, M. Noman, M. Fiaz, and S. Khan, ‘‘COSNet:
| Mar. | 2023, | Art.no.106813. | [Online]. |     | Available: | https://linkinghub. |     |         |          |              |     |         |                |            |
| ---- | ----- | -------------- | --------- | --- | ---------- | ------------------- | --- | ------- | -------- | ------------ | --- | ------- | -------------- | ---------- |
|      |       |                |           |     |            |                     |     | A novel | semantic | segmentation |     | network | using enhanced | boundaries |
elsevier.com/retrieve/pii/S0921344922006450
|     |     |     |     |     |     |     |     | in cluttered | scenes,’’ | in  | Proc. | IEEE/CVF | Winter Conf. | Appl. Com- |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --------- | --- | ----- | -------- | ------------ | ---------- |
[14] N. Basedow, K. Hadasch, M. Dawoud, C. Colloseus, I. Taha, put. Vis. (WACV), Feb. 2025, pp.1363–1372. [Online]. Available:
and D. Aschenbrenner, ‘‘Open data sources for post-consumer https://ieeexplore.ieee.org/abstract/document/10943430
plastic sorting: What we have and what we still need,’’ Proc. [32] A. M. Kirillov, E. Mintun, N. Ravi, H. Mao, C. Rolland,
CIRP, vol. 122, pp.1042–1047, Jan. 2024. [Online]. Available: L. Gustafson, T. Xiao, S. Whitehead, A. C. Berg, W. Lo, P. Dollár,
https://www.sciencedirect.com/science/article/pii/S2212827124001847 and R. Girshick, ‘‘Segment anything,’’ in Proc. IEEE/CVF Int.
|     |     |     |     |     |     |     |     | Conf. | Comput. | Vis., Oct. | 2023, | pp.4015–4026. | [Online]. | Available: |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | ------- | ---------- | ----- | ------------- | --------- | ---------- |
[15] D.Bashkirova,S.Mishra,D.Lteif,P.Teterwak,D.Kim,F.Alladkani,
https://openaccess.thecvf.com/content/ICCV2023/html/Kirillov_
| J. Akl, | B. Çalli, | S. A. Bargal, | K.  | Saenko, | D. Kim, | M. Seo, | Y. Jeon, |     |     |     |     |     |     |     |
| ------- | --------- | ------------- | --- | ------- | ------- | ------- | -------- | --- | --- | --- | --- | --- | --- | --- |
D. Choi, S. Ettedgui, R. Giryes, S. Abu-Hussein, B. Xie, and S. Li, Segment_Anything_ICCV_2023_paper.html
‘‘VisDA2022challenge:Domainadaptationforindustrialwastesorting,’’ [33] Y. Li, Y. Chen, N. Wang, and Z.-X. Zhang, ‘‘Scale-aware trident
inProc.NeurIPSCompetitionsTrack,Aug.2023,pp.104–118.[Online]. networks for object detection,’’ in Proc. IEEE/CVF Int. Conf.
|     |     |     |     |     |     |     |     | Comput. | Vis. | (ICCV), | Oct. 2019, | pp.6053–6062. | [Online]. | Available: |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | ---- | ------- | ---------- | ------------- | --------- | ---------- |
Available:https://proceedings.mlr.press/v220/bashkirova23a.html
https://openaccess.thecvf.com/content_ICCV_2019/html/Li_Scale-
| [16] S. Lynch, | ‘‘OpenLitterMap.Com—Open |     |     | data | on plastic | pollution | with |     |     |     |     |     |     |     |
| -------------- | ------------------------ | --- | --- | ---- | ---------- | --------- | ---- | --- | --- | --- | --- | --- | --- | --- |
Aware_Trident_Networks_for_Object_Detection_ICCV_2019_paper.html
| blockchain | rewards | (Littercoin),’’ |     | Open Geospatial |     | Data, Softw. | Stan- |            |         |        |              |     |         |                    |
| ---------- | ------- | --------------- | --- | --------------- | --- | ------------ | ----- | ---------- | ------- | ------ | ------------ | --- | ------- | ------------------ |
|            |         |                 |     |                 |     |              |       | [34] T.-Y. | Lin, P. | Goyal, | R. Girshick, | K.  | He, and | P. Dollar, ‘‘Focal |
dards,vol.3,no.1,p.6,Jun.2018,doi:10.1186/s40965-018-0050-y.
|     |     |     |     |     |     |     |     | loss | for dense | object | detection,’’ | in  | Proc. IEEE | Int. Conf. |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | --------- | ------ | ------------ | --- | ---------- | ---------- |
[17] Datacluster-labs. (Jul. 2022). Datacluster-labs/Domestic-Trash-Dataset. Comput. Vis. (ICCV), Oct. 2017, pp.2980–2988. [Online].
[Online]. Available: https://github.com/datacluster-labs/Domestic-Trash- Available: https://openaccess.thecvf.com/content_iccv_2017/html/Lin_
Dataset
Focal_Loss_for_ICCV_2017_paper.html
| [18] Y. Cheng, | J.  | Zhu, M. Jiang, | J. Fu, | C. Pang, | P.  | Wang, K. | Sankaran, |                                                                |     |     |     |     |     |     |
| -------------- | --- | -------------- | ------ | -------- | --- | -------- | --------- | -------------------------------------------------------------- | --- | --- | --- | --- | --- | --- |
|                |     |                |        |          |     |          |           | [35] J.RedmonandA.Farhadi,‘‘YOLOv3:Anincrementalimprovement,’’ |     |     |     |     |     |     |
O.Onabola,Y.Liu,D.Liu,andY.Bengio,‘‘FloW:Adatasetandbench-
2018,arXiv:1804.02767.
markforfloatingwastedetectionininlandwaters,’’inProc.IEEE/CVF
|     |     |     |     |     |     |     |     | [36] N. D. | Vo, B. | N. Tran, | H. N. | N. Van, | K. B. T. | Duong, T. V. Le, |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | ------ | -------- | ----- | ------- | -------- | ---------------- |
Int.Conf.Comput.Vis.(ICCV),Montreal,QC,Canada,Oct.2021,p.10. and N.Nguyen, ‘‘Empirical study of real-time one-stage object
[Online].Available:https://ieeexplore.ieee.org/document/9710581/ detection methods on recyclable waste dataset,’’ in Proc. RIVF
[19] J. Bobulski and J. Piatkowski, ‘‘PET waste classification method and Int. Conf. Comput. Commun. Technol. (RIVF), Ho Chi Minh
plasticwasteDataBase–WaDaBa,’’inImageProcessingandCommunica- City, Vietnam, Dec. 2022, pp.268–273. [Online]. Available:
tionsChallenges,M.ChoraśandR.S.Choraś,Eds.,Cham,Switzerland:
https://ieeexplore.ieee.org/document/10013902/
Springer,2017,pp.57–64. [37] A. Bochkovskiy, C.-Y. Wang, and H.-Y. M. Liao, ‘‘YOLOv4: Optimal
[20] D.Mewada,C.Agnew,E.M.Grua,C.Eising,P.Denny,M.Heffernan, speedandaccuracyofobjectdetection,’’2020,arXiv:2004.10934.
K. Tierney, P. van de Ven, and A. Scanlan, ‘‘Contamination detec- [38] G. Jocher. (May 2020). YOLOv5 By Ultralytics. [Online]. Available:
tion from highly cluttered waste scenes using computer vision,’’ https://github.com/ultralytics/yolov5
IEEE Access, vol. 12, pp.129434–129446, 2024. [Online]. Available: [39] C.-Y. Wang, A. Bochkovskiy, and H.-Y.-M. Liao, ‘‘YOLOv7:
https://ieeexplore.ieee.org/abstract/document/10669564 Trainable bag-of-freebies sets new state-of-the-art for real-time
|                 |     |         |          |          |           |     |            | object    | detectors,’’ | in   | Proc. IEEE/CVF |               | Conf. Comput. | Vis. Pattern |
| --------------- | --- | ------- | -------- | -------- | --------- | --- | ---------- | --------- | ------------ | ---- | -------------- | ------------- | ------------- | ------------ |
| [21] Recycleye. |     | (2024). | WasteNet | Dataset. | [Online]. |     | Available: |           |              |      |                |               |               |              |
|                 |     |         |          |          |           |     |            | Recognit. | (CVPR),      | Jun. | 2023,          | pp.7464–7475. | [Online].     | Available:   |
https://recycleye.com/wastenet/
https://openaccess.thecvf.com/content/CVPR2023/html/Wang_
| [22] CVAT.ai | Corporation. | (Nov. | 2023). | Computer | Vision | Annotation | Tool |     |     |     |     |     |     |     |
| ------------ | ------------ | ----- | ------ | -------- | ------ | ---------- | ---- | --- | --- | --- | --- | --- | --- | --- |
YOLOv7_Trainable_Bag-of-Freebies_Sets_New_State-of-the-
(CVAT).[Online].Available:https://github.com/cvat-ai/cvat Art_for_Real-Time_Object_Detectors_CVPR_2023_paper.html
[23] K. Hong, S. Jeon, H. Yang, J. Fu, and H. Byun, ‘‘Domain-aware [40] Q. Chen, Y. Wang, T. Yang, X. Zhang, J. Cheng, and J. Sun,
universal style transfer,’’ in Proc. IEEE/CVF Int. Conf. Comput. ‘‘You only look one-level feature,’’ in Proc. IEEE/CVF Conf. Comput.
| Vis. | (ICCV), | Oct. 2021, | pp.14589–14597. |     | [Online]. |     | Available: |              |           |         |     |            |                 |           |
| ---- | ------- | ---------- | --------------- | --- | --------- | --- | ---------- | ------------ | --------- | ------- | --- | ---------- | --------------- | --------- |
|      |         |            |                 |     |           |     |            | Vis. Pattern | Recognit. | (CVPR), |     | Jun. 2021, | pp.13034–13043. | [Online]. |
https://openaccess.thecvf.com/content/ICCV2021/html/Hong_Domain-
Available:https://openaccess.thecvf.com/content/CVPR2021/html/Chen_
Aware_Universal_Style_Transfer_ICCV_2021_paper.html
You_Only_Look_One-Level_Feature_CVPR_2021_paper.html
| VOLUME13,2025 |     |     |     |     |     |     |     |     |     |     |     |     |     | 151951 |
| ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |

P.Thielmannetal.:ReviewofComputerVisionforIndustrial-GradeWasteClassification
[41] V. Prasad and M. Arashpour, ‘‘Optimally leveraging depth [55] K. Duan, S. Bai, L. Xie, H. Qi, Q. Huang, and Q. Tian, ‘‘CenterNet:
features to enhance segmentation of recyclables from Keypoint triplets for object detection,’’ in Proc. IEEE/CVF Int. Conf.
cluttered construction and demolition waste streams,’’ J. Comput. Vis. (ICCV), Oct. 2019, pp.6569–6578. [Online]. Available:
Environ. Manage., vol. 354, Mar. 2024, Art.no.120313. https://openaccess.thecvf.com/content_ICCV_2019/html/Duan_
[Online]. Available: https://linkinghub.elsevier.com/retrieve/pii/ CenterNet_Keypoint_Triplets_for_Object_Detection_ICCV_2019_paper.
| S0301479724002998 |     |     |     |     |     |     |     | html |     |     |     |     |     |     |     |
| ----------------- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
[42] M. Z. Ali, O. Alsuwaidi, and S. Khan, ‘‘Enhanced segmentation of [56] Z.Ge,S.Liu,F.Wang,Z.Li,andJ.Sun,‘‘YOLOX:ExceedingYOLO
deformed waste objects in cluttered environments,’’ in Proc. 13th Int. seriesin2021,’’2021,arXiv:2107.08430.
Conf., 2024, pp.570–581. [Online]. Available: https://www.scitepress. [57] S. Ren, K. He, R. Girshick, and J. Sun, ‘‘Faster R-CNN: Towards
org/DigitalLibrary/Link.aspx?doi=10.5220/0012424900003654 real-time object detection with region proposal networks,’’ in
|                 |     |             |     |           |     |             |       | Proc. | Adv. Neural | Inf. | Process. | Syst., | vol. 28, | 2015, pp.91–99. |     |
| --------------- | --- | ----------- | --- | --------- | --- | ----------- | ----- | ----- | ----------- | ---- | -------- | ------ | -------- | --------------- | --- |
| [43] J. Redmon, |     | S. Divvala, | R.  | Girshick, | and | A. Farhadi, | ‘‘You |       |             |      |          |        |          |                 |     |
only look once: Unified, real-time object detection,’’ in Proc. [Online]. Available: https://proceedings.neurips.cc/paper/2015/hash/
IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR), Jun. 2016, 14bfa6bb14875e45bba028a21ed38046-Abstract.html
pp.779–788. [Online]. Available: https://www.cv-foundation.org/ [58] H.Zhang,H.Chang,B.Ma,N.Wang,andX.Chen,‘‘DynamicR-CNN:
openaccess/content_cvpr_2016/html/Redmon_You_Only_Look_ Towardshighqualityobjectdetectionviadynamictraining,’’inComputer
Vision—ECCV.Cham,Switzerland:Springer,2020,pp.260–275.
CVPR_2016_paper.html
|               |     |         |       |           |        |     |             | [59] P. Sun, | R. Zhang, | Y. Jiang, | T.  | Kong, C. | Xu, W. | Zhan, M. Tomizuka, |     |
| ------------- | --- | ------- | ----- | --------- | ------ | --- | ----------- | ------------ | --------- | --------- | --- | -------- | ------ | ------------------ | --- |
| [44] W. Wang, | J.  | Dai, Z. | Chen, | Z. Huang, | Z. Li, | X.  | Zhu, X. Hu, |              |           |           |     |          |        |                    |     |
T. Lu, L. Lu, H. Li, X. Wang, and Y. Qiao, ‘‘InternImage: L.Li,Z.Yuan,C.Wang,andP.Luo,‘‘SparseR-CNN:End-to-endobject
Exploring large-scale vision foundation models with deformable detectionwithlearnableproposals,’’inProc.IEEE/CVFConf.Comput.
convolutions,’’ in Proc. IEEE/CVF Conf. Comput. Vis. Pattern Vis. Pattern Recognit. (CVPR), Jun. 2021, p.14. [Online]. Available:
https://openaccess.thecvf.com/content/CVPR2021/html/Sun_Sparse_R-
| Recognit. | (CVPR), | Jun. | 2023, | pp.14408–14419. |     | [Online]. | Available: |     |     |     |     |     |     |     |     |
| --------- | ------- | ---- | ----- | --------------- | --- | --------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
CNN_End-to-End_Object_Detection_With_Learnable_Proposals_
https://openaccess.thecvf.com/content/CVPR2023/html/Wang_
InternImage_Exploring_Large-Scale_Vision_Foundation_ CVPR_2021_paper.html
Models_With_Deformable_Convolutions_ [60] X. Zhu, W. Su, L. Lu, B. Li, X. Wang, and J. Dai, ‘‘Deformable
CVPR_2023_paper.html DETR: Deformable transformers for end-to-end object
|     |     |     |     |     |     |     |     | detection,’’ | in  | Proc. | Int. Conf., | Oct. | 2020. | [Online]. | Available: |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | ----- | ----------- | ---- | ----- | --------- | ---------- |
[45] V.Petsiuk,A.Das,andK.Saenko,‘‘RISE:Randomizedinputsampling
https://openreview.net/forum?id=gZ9hCDWe6ke
forexplanationofblack-boxmodels,’’2018,arXiv:1806.07421.
[61] I.Alonso,L.Riazuelo,andA.C.Murillo,‘‘MiniNet:Anefficientsemantic
| [46] S. Jo | and | I.-J. Yu, | ‘‘Puzzle-CAM: |     | Improved | localization | via |     |     |     |     |     |     |     |     |
| ---------- | --- | --------- | ------------- | --- | -------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
segmentationConvNetforreal-timeroboticapplications,’’IEEETrans.
| matching | partial | and | full features,’’ | in  | Proc. IEEE | Int. | Conf. Image |     |     |     |     |     |     |     |     |
| -------- | ------- | --- | ---------------- | --- | ---------- | ---- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
Process. (ICIP), Sep. 2021, pp.639–643. [Online]. Available: Robot., vol. 36, no. 4, pp.1340–1347, Aug. 2020. [Online]. Available:
https://ieeexplore.ieee.org/document/9023474
https://ieeexplore.ieee.org/abstract/document/9506058
|                 |                 |          |             |          |               |            |              | [62] E. Xie, | W.           | Wang, Z.             | Yu, A. | Anandkumar,   | J.     | M. Álvarez, | and      |
| --------------- | --------------- | -------- | ----------- | -------- | ------------- | ---------- | ------------ | ------------ | ------------ | -------------------- | ------ | ------------- | ------ | ----------- | -------- |
| [47] S. Lee,    | M.              | Lee, J.  | Lee, and    | H. Shim, | ‘‘Railroad    | is         | not a train: |              |              |                      |        |               |        |             |          |
|                 |                 |          |             |          |               |            |              | P. Luo,      | ‘‘SegFormer: |                      | Simple | and efficient | design | for         | semantic |
| Saliency        | as pseudo-pixel |          | supervision | for      | weakly        | supervised | semantic     |              |              |                      |        |               |        |             |          |
|                 |                 |          |             |          |               |            |              | segmentation |              | with transformers,’’ |        | in Proc.      | Adv.   | Neural Inf. | Process. |
| segmentation,’’ |                 | in Proc. | IEEE/CVF    |          | Conf. Comput. |            | Vis. Pattern |              |              |                      |        |               |        |             |          |
Recognit. (CVPR), Syst., 2021, p.12. [Online]. Available: https://proceedings.neurips.
Jun. 2021, pp.5491–5501. [Online]. Available: cc/paper/2021/hash/64f1f27bf1b4ec22924fd0acb550c235-Abstract.html
https://openaccess.thecvf.com/content/CVPR2021/html/Lee_Railroad_
|     |     |     |     |     |     |     |     | [63] J. Zhang, | H.  | Liu, K. | Yang, | X. Hu, | R. Liu, and | R. Stiefelhagen, |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- | ------- | ----- | ------ | ----------- | ---------------- | --- |
Is_Not_a_Train_Saliency_As_Pseudo-Pixel_Supervision_for_
|     |     |     |     |     |     |     |     | ‘‘CMX: | Cross-modal |     | fusion | for RGB-X | semantic | segmentation |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | ----------- | --- | ------ | --------- | -------- | ------------ | --- |
CVPR_2021_paper.html?ref=https://githubhelp.com
|                |     |          |        |       |                   |     |          | with | transformers,’’     | IEEE | Trans. | Intell. | Transp.         | Syst., | vol. 24,   |
| -------------- | --- | -------- | ------ | ----- | ----------------- | --- | -------- | ---- | ------------------- | ---- | ------ | ------- | --------------- | ------ | ---------- |
| [48] Y. Ouali, | C.  | Hudelot, | and M. | Tami, | ‘‘Semi-supervised |     | semantic |      |                     |      |        |         |                 |        |            |
|                |     |          |        |       |                   |     |          | no.  | 12, pp.14679–14694, |      |        | Dec.    | 2023. [Online]. |        | Available: |
segmentation with cross-consistency training,’’ in Proc. IEEE/CVF https://ieeexplore.ieee.org/abstract/document/10231003
| Conf.           | Comput. | Vis.      | Pattern | Recognit.  | (CVPR),                    |     | Jun. 2020, |                  |     |         |             |     |         |            |          |
| --------------- | ------- | --------- | ------- | ---------- | -------------------------- | --- | ---------- | ---------------- | --- | ------- | ----------- | --- | ------- | ---------- | -------- |
|                 |         |           |         |            |                            |     |            | [64] A. Radford, | J.  | W. Kim, | C. Hallacy, | A.  | Ramesh, | G. Goh, S. | Agarwal, |
| pp.12671–12681. |         | [Online]. |         | Available: | https://openaccess.thecvf. |     |            |                  |     |         |             |     |         |            |          |
G.Sastry,A.Askell,P.Mishkin,J.Clark,G.Krueger,andI.Sutskever,
com/content_CVPR_2020/html/Ouali_Semi-Supervised_
‘‘Learningtransferablevisualmodelsfromnaturallanguagesupervision,’’
Semantic_Segmentation_With_Cross-Consistency_Training_CVPR_2020_
inProc.38thInt.Conf.,Jul.2021,pp.8748–8763.[Online].Available:
paper.html https://proceedings.mlr.press/v139/radford21a.html
[49] S. Liu, S. Zhi, E. Johns, and A. J. Davison, ‘‘Bootstrapping semantic [65] S.S.Jeevanandam,S.Inuganti,S.Govil,D.Stricker,andJ.Rambach,
segmentationwithregionalcontrast,’’2021,arXiv:2104.04465.
‘‘JENGA:Objectselectionandposeestimationforroboticgraspingfroma
[50] J.Qi,M.Nguyen,andW.Q.Yan,‘‘NUNI-waste:Novelsemi-supervised
stack,’’inProc.IEEE/RSJInt.Conf.Intell.RobotsSyst.(IROS),Hangzhou,
| semantic | segmentation |     | waste classification |     | with non-uniform |     | data aug- |     |     |     |     |     |     |     |     |
| -------- | ------------ | --- | -------------------- | --- | ---------------- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
China,Oct.2025.[Online].Available:https://arxiv.org/abs/2506.13425
mentation,’’MultimediaToolsAppl.,vol.83,no.26,pp.68651–68669,
Jan.2024,doi:10.1007/s11042-024-18265-1.
| [51] J. Yang, | C.     | Li, and J.                                                  | Gao, ‘‘Focal | modulation |               | networks,’’ | in Proc.  |     |     |     |     |     |     |     |     |
| ------------- | ------ | ----------------------------------------------------------- | ------------ | ---------- | ------------- | ----------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
| Adv.          | Neural | Inf. Process.                                               | Syst.,       | Dec. 2022, | pp.4203–4217. |             | [Online]. |     |     |     |     |     |     |     |     |
| Available:    |        | https://proceedings.neurips.cc/paper_files/paper/2022/hash/ |              |            |               |             |           |     |     |     |     |     |     |     |     |
1b08f585b0171b74d1401a5195e986f1-Abstract-Conference.
html
| [52] M. Ali, | M.            | Javaid, | M. Noman, | M.           | Fiaz, and    | S. Khan, | ‘‘Fanet:     |     |     |     |     |     |     |     |     |
| ------------ | ------------- | ------- | --------- | ------------ | ------------ | -------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
| Feature      | amplification |         | network   | for semantic | segmentation |          | in cluttered |     |     |     |     |     |     |     |     |
background,’’inProc.IEEEInt.Conf.ImageProcess.(ICIP),AbuDhabi,
| United | Arab | Emirates, | Oct. 2024, | pp.2592–2598. |     | [Online]. | Available: |     |     |     |     |     |     |     |     |
| ------ | ---- | --------- | ---------- | ------------- | --- | --------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
PELLETHIELMANNreceivedtheB.Sc.degreein
https://ieeexplore.ieee.org/document/10647349/
mechanicalengineeringfromTUKaiserslautern,
[53] O.Ronneberger,P.Fischer,andT.Brox,‘‘U-Net:Convolutionalnetworks
|     |     |     |     |     |     |     |     |     |     | in  | 2020, | and the | M.Sc. degree | in mechanical |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | ------- | ------------ | ------------- | --- |
forbiomedicalimagesegmentation,’’inMedicalImageComputingand
|     |     |     |     |     |     |     |     |     |     | engineering |     | with | a minor in | applied | computer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ---- | ---------- | ------- | -------- |
Computer-AssistedIntervention—MICCAI,N.Navab,J.Hornegger,W.M.
Wells, and A. F. Frangi, Eds., Cham, Switzerland: Springer, 2015, sciencefromRPTUKaiserslautern,in2023.
|     |     |     |     |     |     |     |     |     |     |     | He is currently |     | a Researcher | with | the Aug- |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------- | --- | ------------ | ---- | -------- |
pp.234–241.
|                |     |         |         |          |           |            |         |     |     | mented | Vision | Department, |     | German | Research |
| -------------- | --- | ------- | ------- | -------- | --------- | ---------- | ------- | --- | --- | ------ | ------ | ----------- | --- | ------ | -------- |
| [54] S. Zhang, | C.  | Chi, Y. | Yao, Z. | Lei, and | S. Z. Li, | ‘‘Bridging | the gap |     |     |        |        |             |     |        |          |
CenterforArtificialIntelligence(DFKIGmbH),
| between | anchor-based |     | and anchor-free |     | detection     | via adaptive | training     |     |     |                 |     |          |     |             |      |
| ------- | ------------ | --- | --------------- | --- | ------------- | ------------ | ------------ | --- | --- | --------------- | --- | -------- | --- | ----------- | ---- |
|         |              |     |                 |     |               |              |              |     |     | Kaiserslautern, |     | Germany. |     | His current | work |
| sample  | selection,’’ | in  | Proc. IEEE/CVF  |     | Conf. Comput. |              | Vis. Pattern |     |     |                 |     |          |     |             |      |
focusesonapplyingvision-basedlearningmeth-
| Recognit. | (CVPR), | Jun. | 2020, | pp.9759–9768. |     | [Online]. | Available: |     |     |     |     |     |     |     |     |
| --------- | ------- | ---- | ----- | ------------- | --- | --------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
https://openaccess.thecvf.com/content_CVPR_2020/html/Zhang_ ods to real-world industrial and environmental scenarios. His research
Bridging_the_Gap_Between_Anchor-Based_and_Anchor- interestsincludedeeplearningforthecomputervisiondomain,withafocus
Free_Detection_via_Adaptive_CVPR_2020_paper.html onobjectdetectionandsemanticsegmentationinchallengingenvironments.
| 151952 |     |     |     |     |     |     |     |     |     |     |     |     |     | VOLUME13,2025 |     |
| ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------- | --- |

P.Thielmannetal.:ReviewofComputerVisionforIndustrial-GradeWasteClassification
YUZHOUreceivedtheB.Sc.degreeinmechanical DIDIER STRICKER is currently a Professor
engineeringfromHarbinInstituteofTechnology of computer science with Rhineland-Palatinate
(HIT), China, in 2018, and the M.Sc. degree Technical University (RPTU) and the Scientific
in mechatronics and information engineering Director of the German Research Center for
from Karlsruhe Institute of Technology (KIT), Artificial Intelligence (DFKI GmbH), Kaiser-
Germany,in2023. slautern, where he leads the Research Depart-
She is currently a Researcher with the Aug- ment Augmented Vision. From 2011 to 2016,
mented Vision Department, German Research he acted as the Honorary CEO of International
CenterforArtificialIntelligence(DFKIGmbH), Network, GraphicsVision.AI. His research inter-
Kaiserslautern, Germany. Her research interests estsincludecognitiveinterfaces,usermonitoring
include deep learning, human-robot interaction, and CV, with a focus on andon-body-sensor-networks,computervision,video/imageanalytics,and
objectdetectionandinstancesegmentationbasedonfoundationmodelsfor human–computerinteraction.HewasamemberoftheSteeringCommittee,
applicationsacrossvariousdomains. from2000to2007.HereceivedtheInnovationPrizeoftheGermanSociety
of Computer Science, in 2006. He organized as the General Chair the
first2002IEEE&ACMInternationalSymposiumonMixedandAugmented
Reality (ISMAR), Darmstadt, Germany. He got several awards for best
papers or demonstrations at different conferences. He registered several
patents on tracking and augmented reality. He serves as a reviewer for
different European and national research organizations. He is a reviewer
ofdifferentjournalsandconferencesintheareasofVR/ARandcomputer
vision.
BRUNO MIRBACH received the Dr.rer.nat.
degreeintheoreticalphysicsfromtheUniversity
ofKaiserslautern,in1996.
HewasaPostdoctoralResearcherwiththeCen- JASONRAMBACHreceivedthePh.D.degreein
ter for Nonlinear and Complex Systems, Como, computersciencefromtheUniversityofKaiser-
Italy, the Max-Planck-Institute of the Physics of slautern,in2020,forhisdissertationtitled‘‘Learn-
Complex Systems, Dresden, Germany, and the ing Priors for Augmented Reality Tracking and
University of Ulm, Germany, with a research Scene Understanding.’’ He is currently a Senior
focusonnon-lineardynamicsandquantumchaos. ResearcherandtheDeputyDirectorofAugmented
In 1999, he joined the automotive industry, Vision Department, DFKI GmbH, leading the
working on the applied research and development of intelligent optical team‘‘SpatialSensingandMachinePerception’’
sensorsystemsforenvironmentperceptionandoccupantmonitoring.Attwo tacklinggeometric/semanticsceneunderstanding
automotivesuppliers,hehasbeenleadingteamsdedicatedtotheresearch using machine learning. His research interests
anddevelopmentofcomputervisionandmachinelearningalgorithms,with includeSLAMandsemanticsceneunderstanding,objectposeestimationand
numerouspublicationsandtenpatentsin3D-vision,2D/3Dsensorfusion, tracking,anomalydetection,roboticvision,andaugmentedreality.Hehas
andmachinelearning.Since2019,hehasbeenapart-timeSeniorResearcher morethan50publicationsinleadingcomputervisionandaugmentedreality
with the Augmented Vision Department, German Research Center for conferences,theBestPaperAwardfromtheIEEEInternationalSymposium
Artificial Intelligence (DFKI GmbH), Kaiserslautern. He is the author of on Mixed and Augmented Reality (ISMAR), in 2017, and five awards
approximately 80 articles in physics and computer science journals and at the BOP Object Pose Estimation Challenge 2022 and 2023 at ECCV
servesregularlyasareviewerinthesedomains.Hiscurrentresearchinterests andICCV.HeisaReviewerofseveralscientificjournalsandconferences
includemachinelearning,3Dvision,andenvironmentperception,witha (IEEETRANSACTIONSONPATTERNANALYSISANDMACHINEINTELLIGENCE,IEEE
focusonobjectandpersondetectionandposetrackingforapplicationsin TRANSACTIONSONIMAGEPROCESSING,CVPR,ICCV,ECCV,ICRA,WACV,and
variousfields,suchasautomotive,buildingmanagement,construction,and BMVC).
recyclingindustry.
VOLUME13,2025 151953