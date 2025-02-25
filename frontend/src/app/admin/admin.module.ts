import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AdminRoutingModule } from './admin-routing.module';
import { AdminComponent } from './admin.component';
import { HeaderComponent } from './header/header.component';
import { LeftSideComponent } from './left-side/left-side.component';
import { ReadingComponent } from './reading/reading.component';
import { HomeComponent } from './home/home.component';


@NgModule({
  declarations: [
    AdminComponent,
    HeaderComponent,
    LeftSideComponent,
    ReadingComponent,
    HomeComponent
  ],
  imports: [
    CommonModule,
    AdminRoutingModule
  ]
})
export class AdminModule { }
