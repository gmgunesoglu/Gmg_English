import {Component, EventEmitter, Output} from '@angular/core';
import {Unit} from "../../models/unit";
import {FilteredUnit} from "../../models/filtered-unit";
import {ReadingService} from "../../services/reading.service";

@Component({
  selector: 'app-unit',
  templateUrl: './unit.component.html',
  styleUrls: ['./unit.component.scss']
})
export class UnitComponent {

  filtered_units: FilteredUnit[] = []


  constructor(
    private readingService: ReadingService
  ) {}

  ngOnInit(): void {
    this.getUnits()
    console.log(this.filtered_units)
  }

  getUnits(){
    this.readingService.getUnits().subscribe({
      next: (result) => {
        this.filtered_units = result
          .filter(unit => unit.titles.length > 0)
          .map(unit => ({
          ...unit,
          show_titles: false
        }));
      }
    });
  }

  selectUnit(unit: FilteredUnit) {
    console.log("selected unit: " + unit.name)
    unit.show_titles = !unit.show_titles
  }

  selectTitle(titleId: number) {
    this.getTextDetail.emit(titleId);
  }

  @Output() getTextDetail: EventEmitter<number> = new EventEmitter<number>();
}
