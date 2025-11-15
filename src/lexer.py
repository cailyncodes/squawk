"""
Squawk Lexer - Tokenizes source code into a stream of tokens
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional


class TokenType(Enum):
    # Keywords
    FN = auto()
    IF = auto()
    THEN = auto()
    ELSE = auto()
    LET = auto()
    IN = auto()
    RETURN = auto()
    
    # Types
    INT_TYPE = auto()
    BOOL_TYPE = auto()
    
    # Literals
    INTEGER = auto()
    TRUE = auto()
    FALSE = auto()
    
    # Identifiers
    IDENTIFIER = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    EQUALS = auto()
    DOUBLE_EQUALS = auto()
    NOT_EQUALS = auto()
    LESS_THAN = auto()
    GREATER_THAN = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()
    ARROW = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    COMMA = auto()
    COLON = auto()
    SEMICOLON = auto()
    
    # Special
    EOF = auto()
    NEWLINE = auto()


@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
    def error(self, msg: str):
        raise SyntaxError(f"Lexer error at line {self.line}, column {self.column}: {msg}")
    
    def peek(self, offset: int = 0) -> Optional[str]:
        pos = self.pos + offset
        if pos < len(self.source):
            return self.source[pos]
        return None
    
    def advance(self) -> Optional[str]:
        if self.pos < len(self.source):
            ch = self.source[self.pos]
            self.pos += 1
            if ch == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            return ch
        return None
    
    def skip_whitespace(self):
        while self.peek() and self.peek() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        if self.peek() == '#':
            while self.peek() and self.peek() != '\n':
                self.advance()
    
    def read_number(self) -> int:
        num_str = ''
        if self.peek() == '-':
            num_str += self.advance()
        
        while self.peek() and self.peek().isdigit():
            num_str += self.advance()
        
        return int(num_str)
    
    def read_identifier(self) -> str:
        ident = ''
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            ident += self.advance()
        return ident
    
    def add_token(self, token_type: TokenType, value=None):
        self.tokens.append(Token(token_type, value, self.line, self.column))
    
    def tokenize(self) -> List[Token]:
        keywords = {
            'fn': TokenType.FN,
            'if': TokenType.IF,
            'then': TokenType.THEN,
            'else': TokenType.ELSE,
            'let': TokenType.LET,
            'in': TokenType.IN,
            'return': TokenType.RETURN,
            'Int': TokenType.INT_TYPE,
            'Bool': TokenType.BOOL_TYPE,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
        }
        
        while self.pos < len(self.source):
            self.skip_whitespace()
            self.skip_comment()
            
            if self.pos >= len(self.source):
                break
            
            ch = self.peek()
            
            # Newlines
            if ch == '\n':
                self.add_token(TokenType.NEWLINE)
                self.advance()
                continue
            
            # Numbers
            if ch.isdigit() or (ch == '-' and self.peek(1) and self.peek(1).isdigit()):
                num = self.read_number()
                self.add_token(TokenType.INTEGER, num)
                continue
            
            # Identifiers and keywords
            if ch.isalpha() or ch == '_':
                ident = self.read_identifier()
                token_type = keywords.get(ident, TokenType.IDENTIFIER)
                value = None if token_type != TokenType.IDENTIFIER else ident
                if token_type == TokenType.TRUE:
                    value = True
                elif token_type == TokenType.FALSE:
                    value = False
                self.add_token(token_type, value)
                continue
            
            # Two-character operators
            if ch == '=' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.add_token(TokenType.DOUBLE_EQUALS)
                continue
            
            if ch == '!' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.add_token(TokenType.NOT_EQUALS)
                continue
            
            if ch == '<' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.add_token(TokenType.LESS_EQUAL)
                continue
            
            if ch == '>' and self.peek(1) == '=':
                self.advance()
                self.advance()
                self.add_token(TokenType.GREATER_EQUAL)
                continue
            
            if ch == '-' and self.peek(1) == '>':
                self.advance()
                self.advance()
                self.add_token(TokenType.ARROW)
                continue
            
            # Single-character tokens
            single_char = {
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                '=': TokenType.EQUALS,
                '<': TokenType.LESS_THAN,
                '>': TokenType.GREATER_THAN,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '{': TokenType.LBRACE,
                '}': TokenType.RBRACE,
                ',': TokenType.COMMA,
                ':': TokenType.COLON,
                ';': TokenType.SEMICOLON,
            }
            
            if ch in single_char:
                self.add_token(single_char[ch])
                self.advance()
                continue
            
            self.error(f"Unexpected character: {ch}")
        
        self.add_token(TokenType.EOF)
        return self.tokens
