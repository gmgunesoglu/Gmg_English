import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Unit} from "../../../models/unit";
import {CreateUnit} from "../../../models/create-unit";
import {ReadingService} from "../../../services/reading.service";


@Component({
  selector: 'app-unit-create',
  templateUrl: './unit-create.component.html',
  styleUrls: ['./unit-create.component.scss']
})
export class UnitCreateComponent {

  create_unit: CreateUnit = {
    title: "",
  }


  constructor(
    private readingService: ReadingService
  ) {}


  @Output() continueCreate: EventEmitter<Unit> = new EventEmitter<Unit>();
  @Output() back: EventEmitter<void> = new EventEmitter<void>();


  createNewUnit(): void {
    if (!this.create_unit.title.trim()) return;
    this.readingService.createUnit(this.create_unit).subscribe(
      (unit) => {
        this.create_unit.title = '';
        this.continueCreate.emit(unit)
      },
      (error) =>  alert(error.error.detail)
    );

  }

  cancelCreatNewUnit() {
    this.back.emit()
  }

}
