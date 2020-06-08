#encoding "utf-8"
#GRAMMAR_ROOT PersonFullName

PersonFullName -> BocharovAndreiIvanovich_familyname BocharovAndreiIvanovich_name BocharovAndreiIvanovich_fathername |
BocharovAndreiIvanovich_familyname BocharovAndreiIvanovich_name | 
BocharovAndreiIvanovich_name BocharovAndreiIvanovich_familyname;
BocharovAndreiIvanovich_name -> "андрей";
BocharovAndreiIvanovich_familyname -> "бочаров";
BocharovAndreiIvanovich_fathername ->"иванович"; 


// компоненты даты
// Day -> AnyWord<wff=/([1-2]?[0-9])|(3[0-1])/>;
// Month -> Noun<kwtype="месяц">;
// YearRecentNum -> AnyWord<wff=/((1[6-9])|(20))[0-9]{2}/>;
// YearSinNum -> AnyWord<wff=/[1-2][0-9]{1,3}/>;
// YearSinDesc -> "год" | "г." | "г";
// YearPluralNum -> AnyWord<wff=/[0-9]{2,4}((-ые)|(-е)|(-ых)|(-х))/>;
// YearPluralDesc -> "год" | "гг" | "гг.";
// YearNum -> YearSinNum | YearPluralNum;
// YearDesc -> YearSinDesc | YearPluralDesc;
// CenturyNum -> AnyWord<wff=/[XVI]{1,5}/>;
// CenturyDesc -> "век" | "в." | "вв";
// Era -> "н" "." "э" "." | "до" "н" "." "э" ".";
// PeriodWord -> "середина" | "начало" | "конец";
// Period -> Prep PeriodWord | PeriodWord;

// Date -> Day interp (Date.Day)
//         Month interp (Date.Month)
//         (Year interp (Date.Year));
// Date -> Month interp (Date.Month)
//         Year interp (Date.Year);
// Date -> Year interp (Date.Year);
// Date -> Century interp (Date.Century);

// исключения
// Date -> NotAYear; // никуда не записывается
// NotAYear -> "ibm" YearRecentNum;// IBM 1620
// NotAYear -> YearSinNum Noun<gram="gen">;    // 2000 экземпляров
// NotAYear -> YearSinNum Adj Noun<gram="gen">;// 2000 10-знаковых слов

// форматы даты
// Year -> npYear | pYear | Prep pYear; // перед pYear может стоять предлог
// npYear -> Prep YearSinNum Prep YearSinNum YearDesc;     // с 1234 по 2345 годы
// npYear -> Prep YearSinNum SimConjAnd YearSinNum YearDesc;//между 1951 и 1957 годами
// npYear -> Period YearPluralNum;                         // в начале 30-х годов
// pYear -> YearNum Hyphen YearNum YearDesc;               // 1234 — 2345 годы
// pYear -> YearNum Hyphen YearNum;                        // 1234 — 2345
// pYear -> YearPluralNum YearPluralDesc;                  // 1230-е годы
// pYear -> YearPluralNum;                                 // 30-е
// pYear -> Period YearPluralNum YearPluralDesc;           // конец 30-х годов
// pYear -> YearSinNum YearSinDesc Era;                    // 60 г. до н.э.
// pYear -> YearSinNum YearSinDesc;                        // 1960 год
// pYear -> YearRecentNum;                                 // 1960
// Century -> Period CenturyNum CenturyDesc;               // в начале XX века
// Century -> Prep CenturyNum CenturyDesc;                 // в XX веке
// Century -> CenturyNum CenturyDesc;                      // XX век