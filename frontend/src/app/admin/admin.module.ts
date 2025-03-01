import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DragDropModule } from '@angular/cdk/drag-drop';

import { AdminRoutingModule } from './admin-routing.module';
import { AdminComponent } from './admin.component';
import { HeaderComponent } from './header/header.component';
import { LeftSideComponent } from './left-side/left-side.component';
import { ReadingComponent } from './reading/reading.component';
import { HomeComponent } from './home/home.component';
import {FormsModule} from "@angular/forms";
import { TextComponent } from './reading/text/text.component';
import { UnitComponent } from './reading/unit/unit.component';
import { UnitCreateComponent } from './reading/unit-create/unit-create.component';
import { TextCreateComponent } from './reading/text-create/text-create.component';


@NgModule({
  declarations: [
    AdminComponent,
    HeaderComponent,
    LeftSideComponent,
    ReadingComponent,
    HomeComponent,
    TextComponent,
    UnitComponent,
    UnitCreateComponent,
    TextCreateComponent
  ],
  imports: [
    CommonModule,
    AdminRoutingModule,
    FormsModule,
    DragDropModule
  ]
})
export class AdminModule { }
