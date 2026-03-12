# SCA-German Forms

This folder contains bilingual (English / German) CSV data files for SCA (Specific
Client Audit) forms used in the DACH region (Germany, Austria, Switzerland).
Files include a Linxon capacity assessment and 54 Austria-specific occupational
health and safety audit forms covering topics from abrasive blasting to workplace
conditions, aligned with Austrian labor law and EU directives.

## CSV File Structure

Each CSV file contains the following columns:
- `_id`: MongoDB document ID
- `mongoId`: MongoDB reference ID
- `avettaId`: Avetta internal ID (matches formDisplayId for the top-level form group)
- `mongoObject`: Object type — `questionGroup` or `question`
- `field`: Field type — `questionGroupText`, `questionText`, `description`, `responseOption*`
- `formDisplayId`: The form's display ID (matches the formID in the filename)
- `questionGroupType`: Always `form` for top-level entries
- `en`: English text content
- `de` *(optional)*: German text content — present in all files in this folder

## Form Index

| formID | form name | form description | Country | Region |
|--------|-----------|-----------------|---------|--------|
| 40082 | Linxon - Capacity & Capability - Specific | Assesses company capacity and capability across building infrastructure, employee experience, major equipment, and technical competencies for vendor/contractor qualification. | Germany | EMEA |
| 51136 | Austria - Company Safety Details and Instructions | Identifies work types performed by the company to customize safety audit requirements, covering diverse construction and specialized services. | Austria | EMEA |
| 51137 | Harris SDI Questionnaire | Collects financial and bonding information for vendors planning significant contract value with Harris, including balance sheet, income statement, WIP, and contract backlog details. | Global | EMEA |
| 51139 | Construction - Abrasive Blasting | Verifies compliance with Austrian construction safety requirements for abrasive blasting operations including respiratory protection and dust control. | Austria | EMEA |
| 51140 | Construction - Concrete Equipment | Ensures safe operation of concrete mixing and spraying equipment with proper securement, energy isolation, and operator training. | Austria | EMEA |
| 51141 | Construction - Confined Spaces | Establishes procedures for safe entry and work in confined spaces including hazard assessment, ventilation, and rescue arrangements. | Austria | EMEA |
| 51142 | Construction - Demolition | Covers pre-demolition structural evaluation, hazardous substance removal, utility location, and controlled debris management. | Austria | EMEA |
| 51143 | Construction - Equipment | Implements equipment inspection and maintenance programs with qualified personnel and annual safety assessments. | Austria | EMEA |
| 51144 | Construction - Fire and Explosion Prevention | Prevents fire and explosion risks through ignition controls, flammable waste removal, and fire equipment maintenance. | Austria | EMEA |
| 51145 | Construction - Hoists | Ensures secure hoist installation, load signaling, access control, and guarding of moving parts on construction sites. | Austria | EMEA |
| 51146 | Construction - Lead | Manages lead paint and dust exposure through application restrictions, dust control, respiratory protection, and hygiene provisions. | Austria | EMEA |
| 51147 | Construction - Lifting Operations | Requires pre-lift equipment inspections, safe load attachment, and verification of equipment suitability before lifting work. | Austria | EMEA |
| 51148 | Construction - Management | Establishes site management controls including labor inspectorate notification, employee fitness, multi-employer coordination, and site supervision. | Austria | EMEA |
| 51149 | Construction - Material Handling and Storage | Secures material storage against falling hazards with height limits, stable foundations, and authorized drop zones. | Austria | EMEA |
| 51150 | Construction - Scaffolding | Ensures scaffolding load capacity, safe access, regular inspections, and qualified personnel for erection and dismantling. | Austria | EMEA |
| 51151 | Construction - Training | Requires site safety induction before work and annual refresher training with updates after incidents or changes. | Austria | EMEA |
| 51152 | Construction - Underground Mining | Establishes comprehensive underground work safety including daily inspections, ventilation, gas monitoring, and emergency procedures. | Austria | EMEA |
| 51153 | Cranes | Controls crane operation through communication rules, operator qualifications, access restrictions, and daily safety inspections. | Austria | EMEA |
| 51154 | Electrical Safety | Ensures electrical work is performed by qualified personnel with proper equipment suitability, insulation, fault protection, and testing. | Austria | EMEA |
| 51155 | Electromagnetic Fields (EMF) | Assesses and controls electromagnetic field exposure with exposure limits, protective measures, and employee training. | Austria | EMEA |
| 51156 | Emergency Preparedness and Response | Establishes emergency procedures including notification, evacuation drills, escape routes, and emergency equipment maintenance. | Austria | EMEA |
| 51157 | Excavations | Manages excavation hazards through utility identification, slope support, edge protection, and shoring inspections. | Austria | EMEA |
| 51158 | Explosive Atmospheres | Prevents explosive atmosphere incidents through hazard assessment, zoning, work authorization, and atmospheric monitoring. | Austria | EMEA |
| 51159 | Explosives | Regulates explosives possession, qualified blasters, secure storage, disposal, and detailed record-keeping. | Austria | EMEA |
| 51160 | Fall Protection | Implements fall protection above specified heights with collective measures prioritized and edge zone restrictions. | Austria | EMEA |
| 51161 | Fire Safety | Establishes fire prevention with trained personnel, fire safety officers, equipment maintenance, and annual evacuation drills. | Austria | EMEA |
| 51162 | First Aid | Ensures adequate first aid training, supplies, and trained personnel based on workforce size and hazard levels. | Austria | EMEA |
| 51163 | Hazardous Substances | Controls hazardous substance exposure through assessment, safe handling, labeling, storage, and health monitoring. | Austria | EMEA |
| 51164 | Hazardous Substances - Carcinogens, Mutagens, Reprotoxic Substances | Manages exposure to carcinogenic and reprotoxic substances with restricted access, exposure registers, and labor inspectorate notification. | Austria | EMEA |
| 51165 | Health Monitoring | Implements medical examinations for occupational disease risk with pre-work and periodic assessments plus reporting. | Austria | EMEA |
| 51166 | Heat and Ultraviolet (UV) Radiation | Protects workers from heat and UV exposure through risk assessment, control measures, first aid, and medical examinations. | Austria | EMEA |
| 51167 | Hot Work | Prevents fire hazards from welding and cutting through training, cylinder securement, fire prevention measures, and fire watch. | Austria | EMEA |
| 51168 | Hyperbaric Work | Establishes comprehensive pressurized air work protocols with qualified supervision, medical fitness, equipment testing, and rescue arrangements. | Austria | EMEA |
| 51169 | Hyperbaric Work - Diving | Implements diving safety through team composition, qualified supervision, equipment inspections, pre-dive briefings, and annual medical certification. | Austria | EMEA |
| 51170 | Incident Recording and Reporting | Requires immediate incident reporting, record retention, and timely reporting to accident insurance authorities. | Austria | EMEA |
| 51171 | Ionizing Radiation | Controls ionizing radiation exposure with workplace monitoring, dose limits, protective measures, access control, and medical examinations. | Austria | EMEA |
| 51172 | Ladders | Ensures ladder safety through secure positioning, handhold requirements, and additional protection for work at height. | Austria | EMEA |
| 51173 | Lifting Equipment | Establishes lifting equipment safety with supervised assembly/dismantling, load limits, and stability measures. | Austria | EMEA |
| 51174 | Manual Handling and Storage | Minimizes manual handling through mechanical aids with hazard assessment, control measures, training, and safe storage. | Austria | EMEA |
| 51175 | Multi-Employer Coordination | Coordinates safety among multiple employers at shared workplaces with hazard information sharing and worker training. | Austria | EMEA |
| 51176 | Noise | Manages noise exposure through assessment, hearing protection, exposure limits, hearing examinations, and exposure registers. | Austria | EMEA |
| 51177 | Occupational Health and Safety Committee | Establishes workplace safety committee with minimum annual meetings for workplaces with 100+ employees. | Austria | EMEA |
| 51178 | Optical Radiation | Controls optical radiation hazards through exposure assessment, limit compliance, and protective measures. | Austria | EMEA |
| 51179 | Personal Protective Equipment (PPE) | Ensures proper PPE selection, provision, fit, maintenance, and training for all identified hazards. | Austria | EMEA |
| 51180 | Respiratory Protection | Provides respiratory protection with medical examinations, proper training, semi-annual drills, and quarterly equipment inspections. | Austria | EMEA |
| 51181 | Risk Assessment and Hazard Prevention | Implements comprehensive hazard identification, assessment, documented controls, and regular review of safety measures. | Austria | EMEA |
| 51182 | Road Transportation - Dangerous Goods | Regulates dangerous goods transport with consignor classification, transport documents, approved packaging, and driver training. | Austria | EMEA |
| 51183 | Road Work | Establishes safety requirements for road construction and maintenance work including traffic management and worker protection. | Austria | EMEA |
| 51184 | Roof Work | Ensures roof work safety with fall protection measures, qualified personnel, and special precautions for steep or hazardous surfaces. | Austria | EMEA |
| 51185 | Traffic Safety | Implements traffic safety through control measures, high-visibility clothing, designated routes, and clearance specifications. | Austria | EMEA |
| 51186 | Training | Requires general safety instructions before work commencement with refresher training after changes or incidents in understandable language. | Austria | EMEA |
| 51187 | Vibration | Manages vibration exposure through assessment, exposure limits, control measures, restricted access, and training. | Austria | EMEA |
| 51188 | Work Equipment | Ensures equipment safety through pre-use inspections, maintenance, training, and acceptance testing before use. | Austria | EMEA |
| 51189 | Working On, Over, or Near Water | Provides water safety through rescue equipment, trained personnel, emergency drills, and rescue boats for high-risk operations. | Austria | EMEA |
| 51190 | Workplace Conditions | Maintains safe workplace conditions with employee consultation, safety representatives, hazard signage, ventilation, lighting, and hygiene facilities. | Austria | EMEA |