import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {CdkDragDrop, moveItemInArray, transferArrayItem} from "@angular/cdk/drag-drop";

interface Title {
  id: number;
  title: string;
}

interface Unit {
  id: number;
  name: string;
  titles: Title[];
  showTitles: boolean;
}

interface Quest {
  id: number;
  quest: string;
  option_a: string;
  option_b: string;
  option_c: string;
  option_d: string;
  correct_option: string;
  justification: string;
}

interface TextData {
  id: number;
  unit_name: string;
  title: string;
  context: string;
  quests: Quest[];
}


@Component({
  selector: 'app-reading',
  templateUrl: './reading.component.html',
  styleUrls: ['./reading.component.scss']
})
export class ReadingComponent implements OnInit {
  filteredUnits: Unit[] = [];
  units: Unit[] = [];
  showForm: boolean = false;
  selectedText: TextData | null = null;
  isListingUnits: boolean = true
  unitStart: string = ""
  titleStart: string = ""
  isCreatingUnit: boolean = false

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
    this.fetchUnits();
    this.filteredUnits.forEach(unit => {
      unit.showTitles = true;
    });
  }

  fetchUnits(): void {
    this.http.get<Unit[]>('http://localhost:8000/readings/units').subscribe(
      (data) => {
        this.units = data.map(unit => ({
          ...unit,
          showTitles: true
        }));
        this.filteredUnits = data.map(unit => ({
          ...unit,
          showTitles: true
        }));
      },
      (error) => console.error('Error fetching units:', error)
    );
  }

  toggleForm(): void {
    this.isCreatingUnit = true;
  }

  loadText(titleId: number): void {
    this.http.get<TextData>(`http://localhost:8000/readings/texts/${titleId}`).subscribe(
      (data) => this.selectedText = data,
      (error) => console.error('Error fetching text:', error)
    );
  }

  filterUnitsWithUnitNameAndTitle() {
    this.filteredUnits = this.units.filter(unit => unit.name.startsWith(this.unitStart))
      .map(unit => ({
        ...unit,
        titles: unit.titles.filter(title => title.title.startsWith(this.titleStart))
      }));
  }

  cancelCreatingNewUnit() {
    this.isCreatingUnit = false
  }


  // Title'ları açma ve kapama işlevi
  toggleTitles(unit: Unit, i: number): void {
    unit.showTitles = !unit.showTitles;
    this.units[i].showTitles = unit.showTitles
  }

  // Unit detayları gösterme
  viewUnitDetails(unit: Unit): void {
    console.log('Viewing details for unit: ', unit);
    // Detaylar gösterme işlemi
  }

  // Unit güncelleme
  updateUnit(unit: Unit): void {
    console.log('Updating unit: ', unit);
    // Güncelleme işlemi
  }

  // Unit silme
  deleteUnit(unit: Unit): void {
    console.log('Deleting unit: ', unit);
    this.http.delete<string>(`http://localhost:8000/readings/units/${unit.id}`).subscribe(
      (message) => {
        console.log('Server response:', message);
        this.fetchUnits()
        alert(message); // Gelen mesajı bir uyarı olarak göster
      },
      (error) => console.error('Error fetching text:', error)
    );
  }

  drop(event: CdkDragDrop<any[]>, targetUnit: any) {
    const previousUnit = this.filteredUnits.find(unit => unit.titles === event.previousContainer.data);

    if (!previousUnit) return;

    if (event.previousContainer === event.container) {
      // Aynı unit içinde sıralama değişikliği
      moveItemInArray(targetUnit.titles, event.previousIndex, event.currentIndex);
    } else {
      // Başka bir unit'e taşıma işlemi
      transferArrayItem(
        event.previousContainer.data, // Kaynak unit'in titles listesi
        event.container.data, // Hedef unit'in titles listesi
        event.previousIndex,
        event.currentIndex
      );
    }
  }
}
