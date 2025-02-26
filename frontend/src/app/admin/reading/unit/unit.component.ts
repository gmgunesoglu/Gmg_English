import {Component, Input} from '@angular/core';


interface Title {
  id: number;
  title: string;
}

interface Unit {
  id: number;
  name: string;
  titles: Title[];
}

@Component({
  selector: 'app-unit',
  templateUrl: './unit.component.html',
  styleUrls: ['./unit.component.scss']
})
export class UnitComponent {

  @Input() unit!: Unit;
}
