import {Component, EventEmitter, Output} from '@angular/core';
import {Unit} from "../../models/unit";
import {ReadingService} from "../../services/reading.service";

@Component({
  selector: 'app-unit',
  templateUrl: './unit.component.html',
  styleUrls: ['./unit.component.scss']
})
export class UnitComponent {

  units: Array<Unit> = []


  constructor(
    private readingService: ReadingService
  ) {}

  ngOnInit(): void {
    this.getUnits()
    console.log(this.units)
  }

  getUnits(){
    this.readingService.getUnits().subscribe({
      next: (result) => {
        this.units = result
      }
    });
  }

  selectUnit(unit: Unit) {
    console.log("selected unit: " + unit.name)
    unit.showTitles = !unit.showTitles
  }

  selectTitle(titleId: number) {
    this.getTextDetail.emit(titleId);
  }

  @Output() getTextDetail: EventEmitter<number> = new EventEmitter<number>();
}
