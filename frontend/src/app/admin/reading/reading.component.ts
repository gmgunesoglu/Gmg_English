import {Component, OnInit, Optional} from '@angular/core';
import {CdkDragDrop, moveItemInArray, transferArrayItem} from "@angular/cdk/drag-drop";
import {Title} from "../../models/title";
import {Unit} from "../../models/unit";
import {FilteredUnit} from "../../models/filtered-unit";
import {TextDetail} from "../../models/text-detail";
import {ReadingService} from "../../services/reading.service";
import {CreatedText} from "../../models/created-text";


@Component({
  selector: 'app-reading',
  templateUrl: './reading.component.html',
  styleUrls: ['./reading.component.scss']
})
export class ReadingComponent implements OnInit {
  selected_unit!: Unit;
  filtered_units: FilteredUnit[] = [];
  units: FilteredUnit[] = [];
  isListingUnits: boolean = true;
  isCreatingText: boolean = false;
  unitStart: string = "";
  titleStart: string = "";
  isCreatingUnit: boolean = false;
  isTextDetail: boolean = false;
  text_detail!: TextDetail;


  constructor(
    private readingService: ReadingService
  ) {}

  ngOnInit(): void {
    this.fetchUnits();
  }


  fetchUnits(): void {
    this.readingService.getUnits().subscribe(
      (result) => {
        this.units = result.map(unit => ({
          ...unit,
          show_titles: true
        }));
        this.filtered_units = result.map(unit => ({
          ...unit,
          show_titles: true
        }));
      },
      (error) => console.error('Error fetching units:', error)
    );
  }

  openFormCreatingUnit(): void {
    this.isCreatingUnit = true;
    this.isListingUnits = false
    this.isCreatingText = false;
  }

  filterUnitsWithUnitNameAndTitle() {
    this.filtered_units = this.units.filter(unit => unit.name.startsWith(this.unitStart))
      .map(unit => ({
        ...unit,
        titles: unit.titles.filter(title => title.name.startsWith(this.titleStart))
      }));
  }

  listUnits() {
    this.isListingUnits = true;
    this.isCreatingUnit = false;
    this.isCreatingText = false;
    this.isTextDetail = false;
  }

  openTitles(unit: FilteredUnit, i: number): void {
    unit.show_titles = true;
    this.units[i].show_titles = true;
  }
  closeTitles(unit: FilteredUnit, i: number): void {
    unit.show_titles = false;
    this.units[i].show_titles = false;
  }

  getTextDetail(unit: Unit): void {
    console.log('Viewing details for unit: ', unit);
    this.readingService.getTextDetail(unit.id).subscribe(
      (result) => {
      this.text_detail = result;
      this.isListingUnits = false;
      this.isTextDetail = true;
    });

  }

  updateUnit(unit: Unit): void {
    console.log('Updating unit: ', unit);
    // Güncelleme işlemi
  }

  deleteUnit(unit: Unit): void {
    console.log('Deleting unit: ', unit);
    this.readingService.deleteUnit(unit.id).subscribe(
      (message) => {
        console.log('Server response:', message);
        this.fetchUnits()
        alert(message); // Gelen mesajı bir uyarı olarak göster
      },
      (error) => console.error('Error fetching text:', error)
    );
  }

  drop(event: CdkDragDrop<any[]>, targetUnit: any) {
    const previousUnit = this.filtered_units.find(unit => unit.titles === event.previousContainer.data);

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

  createText(unit: Unit) {
    this.selected_unit = unit;
    console.log("selected unit: ", unit);
    this.isListingUnits = false;
    this.isCreatingUnit = false;
    this.isCreatingUnit = false;
    this.isCreatingText = true;
  }

  stopCreating(created_text: CreatedText) {
    this.fetchUnits()
    this.listUnits()
  }

  deleteText(title: Title) {
    console.log('Deleting title: ', title);
    this.readingService.deleteText(title.id).subscribe(
      (message) => {
        console.log('Server response:', message);
        this.fetchUnits()
        alert(message); // Gelen mesajı bir uyarı olarak göster
      },
      (error) => console.error('Error fetching text:', error)
    );
  }
}
