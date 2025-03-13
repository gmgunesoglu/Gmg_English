import { Component, Input, Output, EventEmitter } from '@angular/core';
import {TextDetail} from "../../../models/text-detail";


@Component({
  selector: 'app-text',
  templateUrl: './text.component.html',
  styleUrls: ['./text.component.scss']
})
export class TextComponent {
  @Input() text_detail!: TextDetail;
  @Output() back = new EventEmitter<void>();

  closeText(): void {
    this.back.emit();
  }
}
