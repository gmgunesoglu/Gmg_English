import {Component, EventEmitter, OnInit, Output} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Unit} from "../../../models/unit";


@Component({
  selector: 'app-unit-create',
  templateUrl: './unit-create.component.html',
  styleUrls: ['./unit-create.component.scss']
})
export class UnitCreateComponent {

  constructor(private http: HttpClient) {}
  newUnitName: string = "";

  @Output() continueCreate: EventEmitter<Unit> = new EventEmitter<Unit>();
  @Output() cancelCreate: EventEmitter<void> = new EventEmitter<void>();

  createNewUnit(): void {
    if (!this.newUnitName.trim()) return;
    const payload = { title: this.newUnitName };
    this.http.post<Unit>('http://localhost:8000/readings/units', payload).subscribe(
      (unit) => {
        this.newUnitName = '';
        // this.fetchUnits();
        // alert(message); // Gelen mesajı bir uyarı olarak göster
        this.continueCreate.emit(unit)
      },
      (error) =>  alert(error.error.detail)
    );
  }

  cancelCreatNewUnit() {
    this.cancelCreate.emit()
  }

}
